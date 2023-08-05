# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.root import getNavigationRoot
from Products.Five import BrowserView
from logging import getLogger
from plone.app.content.utils import json_dumps
from plone.app.content.utils import json_loads
from plone.app.querystring import queryparser
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.supermodel.utils import mergedTaggedValueDict
from types import FunctionType
from zope.component import getUtility
from zope.component import queryAdapter
from zope.component import queryUtility
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IVocabularyFactory
from zope.security.interfaces import IPermission
from Products.CMFPlone import PloneMessageFactory as _
from zope.i18n import translate
from Products.CMFPlone.utils import safe_unicode
import inspect
import itertools

logger = getLogger(__name__)

MAX_BATCH_SIZE = 500  # prevent overloading server

_permissions = {
    'plone.app.vocabularies.Users': 'Modify portal content',
    'plone.app.vocabularies.Catalog': 'View',
    'plone.app.vocabularies.Keywords': 'Modify portal content',
    'plone.app.vocabularies.SyndicatableFeedItems': 'Modify portal content'
}


def _parseJSON(s):
    if isinstance(s, basestring):
        s = s.strip()
        if (s.startswith('{') and s.endswith('}')) or \
                (s.startswith('[') and s.endswith(']')):  # detect if json
            return json_loads(s)
    return s


_unsafe_metadata = ['Creator', 'listCreators', 'author_name', 'commentors']
_safe_callable_metadata = ['getURL', 'getPath','review_state',
                            'getIcon', 'is_folderish']


class VocabLookupException(Exception):
    pass


class BaseVocabularyView(BrowserView):

    def __call__(self):
        """
        Accepts GET parameters of:
        name: Name of the vocabulary
        field: Name of the field the vocabulary is being retrieved for
        query: string or json object of criteria and options.
            json value consists of a structure:
                {
                    criteria: object,
                    sort_on: index,
                    sort_order: (asc|reversed)
                }
        attributes: comma seperated, or json object list
        batch: {
            page: 1-based page of results,
            size: size of paged results
        }
        """
        context = self.get_context()
        self.request.response.setHeader("Content-type", "application/json")

        try:
            vocabulary = self.get_vocabulary()
        except VocabLookupException, e:
            return json_dumps({'error': e.message})

        results_are_brains = False
        if hasattr(vocabulary, 'search_catalog'):
            query = self.parsed_query()
            results = vocabulary.search_catalog(query)
            results_are_brains = True
        elif hasattr(vocabulary, 'search'):
            try:
                query = self.parsed_query()['SearchableText']['query']
            except KeyError:
                results = iter(vocabulary)
            else:
                results = vocabulary.search(query)
        else:
            results = vocabulary

        try:
            total = len(results)
        except TypeError:
            # do not error if object does not support __len__
            # we'll check again later if we can figure some size
            # out
            total = 0

        # get batch
        batch = _parseJSON(self.request.get('batch', ''))
        if batch and ('size' not in batch or 'page' not in batch):
            batch = None  # batching not providing correct options
        if batch:
            # must be slicable for batching support
            page = int(batch['page'])
            size = int(batch['size'])
            if size > MAX_BATCH_SIZE:
                raise Exception('Max batch size is 500')
            # page is being passed in is 1-based
            start = (max(page - 1, 0)) * size
            end = start + size
            # Try __getitem__-based slice, then iterator slice.
            # The iterator slice has to consume the iterator through
            # to the desired slice, but that shouldn't be the end
            # of the world because at some point the user will hopefully
            # give up scrolling and search instead.
            try:
                results = results[start:end]
            except TypeError:
                results = itertools.islice(results, start, end)

        # build result items
        items = []

        attributes = _parseJSON(self.request.get('attributes', ''))
        if isinstance(attributes, basestring) and attributes:
            attributes = attributes.split(',')

        translate_ignored = [
            'Creator', 'Date', 'Description', 'Title', 'author_name',
            'cmf_uid', 'commentators', 'created', 'effective', 'end',
            'expires', 'getIcon', 'getId', 'getRemoteUrl', 'in_response_to',
            'listCreators', 'location', 'modified', 'start', 'sync_uid',
            'path', 'getURL', 'EffectiveDate', 'getObjSize', 'id',
            'UID', 'ExpirationDate', 'ModificationDate', 'CreationDate',
        ]
        if attributes:
            base_path = getNavigationRoot(context)
            for vocab_item in results:
                if not results_are_brains:
                    vocab_item = vocab_item.value
                item = {}
                for attr in attributes:
                    key = attr
                    if ':' in attr:
                        key, attr = attr.split(':', 1)
                    if attr in _unsafe_metadata:
                        continue
                    if key == 'path':
                        attr = 'getPath'
                    val = getattr(vocab_item, attr, None)
                    if callable(val):
                        if attr in _safe_callable_metadata:
                            val = val()
                        else:
                            continue
                    if key == 'path':
                        val = val[len(base_path):]
                    if key not in translate_ignored and isinstance(val, basestring):
                        item[key] = translate(_(safe_unicode(val)), context=self.request)
                    else:
                        item[key] = val
                items.append(item)
        else:
            for item in results:
                items.append({'id': item.value, 'text': item.title})

        if total == 0:
            total = len(items)

        return json_dumps({
            'results': items,
            'total': total
        })

    def parsed_query(self, ):
        query = _parseJSON(self.request.get('query', ''))
        if isinstance(query, basestring):
            query = {'SearchableText': {'query': query}}
        elif query:
            parsed = queryparser.parseFormquery(
                self.get_context(), query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])
            query = parsed
        else:
            query = {}
        return query


class VocabularyView(BaseVocabularyView):
    """Queries a named vocabulary and returns JSON-formatted results."""

    def get_context(self):
        return self.context

    def get_vocabulary(self):
        # Look up named vocabulary and check permission.

        context = self.context
        factory_name = self.request.get('name', None)
        field_name = self.request.get('field', None)
        if not factory_name:
            raise VocabLookupException('No factory provided.')
        authorized = None
        sm = getSecurityManager()
        if (factory_name not in _permissions or
                not INavigationRoot.providedBy(context)):
            # Check field specific permission
            if field_name:
                permission_checker = queryAdapter(context,
                                                  IFieldPermissionChecker)
                if permission_checker is not None:
                    authorized = permission_checker.validate(field_name,
                                                             factory_name)
                elif sm.checkPermission(_permissions[factory_name], context):
                    # If no checker, fall back to checking the global registry
                    authorized = True

            if not authorized:
                raise VocabLookupException('Vocabulary lookup not allowed')

        # Short circuit if we are on the site root and permission is
        # in global registry
        elif not sm.checkPermission(_permissions[factory_name], context):
            raise VocabLookupException('Vocabulary lookup not allowed')

        factory = queryUtility(IVocabularyFactory, factory_name)
        if not factory:
            raise VocabLookupException(
                'No factory with name "%s" exists.' % factory_name)

        # This part is for backwards-compatibility with the first
        # generation of vocabularies created for plone.app.widgets,
        # which take the (unparsed) query as a parameter of the vocab
        # factory rather than as a separate search method.
        if type(factory) is FunctionType:
            factory_spec = inspect.getargspec(factory)
        else:
            factory_spec = inspect.getargspec(factory.__call__)
        query = _parseJSON(self.request.get('query', ''))
        if query and 'query' in factory_spec.args:
            vocabulary = factory(context, query=query)
        else:
            # This is what is reached for non-legacy vocabularies.
            vocabulary = factory(context)

        return vocabulary


class SourceView(BaseVocabularyView):
    """Queries a field's source and returns JSON-formatted results."""

    def get_context(self):
        return self.context.context

    def get_vocabulary(self):
        widget = self.context
        field = widget.field.bind(widget.context)

        # check field's write permission
        info = mergedTaggedValueDict(field.interface, WRITE_PERMISSIONS_KEY)
        permission_name = info.get(field.__name__, 'cmf.ModifyPortalContent')
        permission = queryUtility(IPermission, name=permission_name)
        if permission is None:
            permission = getUtility(
                IPermission, name='cmf.ModifyPortalContent')
        if not getSecurityManager().checkPermission(
                permission.title, self.get_context()):
            raise VocabLookupException('Vocabulary lookup not allowed.')

        if ICollection.providedBy(field):
            return field.value_type.vocabulary
        else:
            return field.vocabulary
