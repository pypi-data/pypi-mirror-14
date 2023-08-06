import re
import json

import requests

from pydoof.management import ManagementApiClient
from pydoof.search import SearchApiClient

API_KEY = None
"""
The API key to use when authenticating API requests.

The region must be included: token-region
Example: eu1-b42e3ea7c94c93555aa3dcdf2926ead136819518
"""

CLUSTER_REGION = 'eu1'
""" The amazon region doofinder's cluster is in """

MANAGEMENT_DOMAIN = '%s-api.doofinder.com'
""" The management API endpoint to send requests to."""

SEARCH_DOMAIN = '%s-search.doofinder.com'
"""The search API endpoint to send search requests to"""

MANAGEMENT_VERSION = '1'
"""The version of server management API"""

SEARCH_VERSION = '5'
"""The version of server search API"""

SEARCH_HTTPS = True
"""Whether or not search request should be made throug https"""


class SearchEngine(SearchApiClient, ManagementApiClient):
    """
    SearchEngine's basic api management object

    - CRUD operations to search engine's indexed items
    - processing of the search engine's feeds
    - make search requests
    """

    @classmethod
    def all(cls):
        """
        obtain search engines resources for this token

        Returns:
            A list of search engines.
        """
        search_engines = []
        api_root = cls.get_api_root()
        api_root.pop('searchengines')
        for hashid, props in api_root.iteritems():
            search_engines.append(SearchEngine(hashid, name=props['name']))
        return search_engines


    def __init__(self, hashid, name=None, **kwargs):
        self.hashid = hashid
        self.name = name
        super(SearchEngine, self).__init__(**kwargs)

    def get_datatypes(self):
        """
        Get a list of searchengine's datatypes

        Returns:
            list of datatypes
            example:
            ['product', 'page']
        """
        return self.get_types()


    def get_types(self):
        """
        Get a list of searchengine's types

        Returns:
            list of types
            example:
            ['product', 'page']
        """
        result = self.__class__.management_api_call(
            entry_point='%s/types' % self.hashid)
        return result['response']

    def add_type(self, dtype):
        """
        Add a type to the searchengine

        Args:
            dtype (string): name of the type

        Returns:
            list of types with the added one
        """
        result = self.__class__.management_api_call(
            'post', entry_point='%s/types' % self.hashid,
            data=json.dumps({'name': dtype}))

        return result['response']

    def delete_type(self, dtype):
        """
        delete a type and all its items. HANDLE WITH CARE

        Args:
            dtype: the type to delete. all items belonging
                   to that type will be removed. This arg is mandatory

        Returns:
            true on success
        """
        result = self.__class__.management_api_call(
            'delete', entry_point='%s/types/%s' % (self.hashid, dtype))

        if result['status_code'] == requests.codes.NO_CONTENT:
            return True
        else:
            return False

    def items(self, item_type):
        """
        get indexed items iterator

        Args:
            item_type (string): the type of items .

        Returns:
            Items iterator
        """
        return ScrolledItemsIterator(self, item_type)

    def get_item(self, item_type, item_id):
        """
        get details of a specific item
        Args:
            id: value of the identificator field of the item within its type
            item_type: type of the item.
                      if not provided, the search engine's first available datatype is used

        Returns:
            dict representing the item.
        """
        raw_result = self.__class__.management_api_call(
            entry_point='%s/items/%s/%s' % (self.hashid, item_type,
                                            item_id))['response']
        return Item(raw_result)

    def add_item(self, item_type, item_description):
        """
        Add an item to the search engine

        Args:
            item_description: dict or pydoof.Item representing the item to be
                              added
                NOTE: if item's id field not present, one will be created
            item_type: type of the item. If not provided, first one available
                       will be used

        Returns:
            the the id of the created_item, on success
        """
        result = self.__class__.management_api_call(
            'post', entry_point='%s/items/%s' % (self.hashid, item_type),
            data=json.dumps(item_description))

        return self._obtain_id(result['response']['url'])

    def add_items(self, item_type, items_description):
        """
        Add an item to the search engine

        Args:
            items_description (list) list of dict or pydoof.Item representing
                               the items to be added
                NOTE: if item's id field not present, for any item one will be
                      created for it
            item_type (string): type of the items. If not provided, first one
                                available  will be used

        Returns:
            an list with the ids of the created items , on success
        """
        result = self.__class__.management_api_call(
            'post', entry_point='%s/items/%s' % (self.hashid, item_type),
            data=json.dumps(items_description))

        return [ self._obtain_id(item['url']) for item in result['response'] ]


    def update_item(self, item_type, item_id, item_description):
        """
        Update an item of the search engine

        Args:
            item_type: type of the item.
            item_id: id of the item to be updated
            item_description: updated data. dict or Item()
                NOTES:
                  - partial updates not implemented yet
                  - description's id will always be set to item_id,
                  no matter what is posted in description content

        Returns:
            True on success
        """
        result = self.__class__.management_api_call(
            'put', data=json.dumps(item_description),
            entry_point='%s/items/%s/%s' % (self.hashid, item_type, item_id))

    def update_items(self, item_type, items_description):
        """
        Update several items of the search engine

        Args:
            item_type: type of the items.
            items_description: updated data. dict or Item()
                NOTES:
                  - partial updates not implemented
                  - all items have to have id otherwise there'll be an error

        Returns:
            True on success
        """
        result = self.__class__.management_api_call(
            'put', data=json.dumps(items_description),
            entry_point='%s/items/%s' % (self.hashid, item_type))

        if result['status_code'] == 200:
            return True


    def delete_item(self, item_type, item_id):
        """
        delete an item

        Args:
            id: item's unique identificator within its item_type
            item_type: if none the first available datatype is used

        Returns:
            true on success
        """
        result = self.__class__.management_api_call(
            'delete', entry_point='%s/items/%s/%s' % (self.hashid, item_type,
                                                      item_id))

        if result['status_code'] == requests.codes.NO_CONTENT:
            return True
        else:
            return False

    def _get_scrolled_items_page(self, item_type, scroll_id = None):
        """
        Function to obtain internally a scrolled results page,

        Args:
            item_type (string): The type of items to scroll
        Kwargs:
            scroll_id (string): Id of the scroll. If provided, fetch the next page
                                of results. If not, obtain a new scroll
        Returns:
            Dict with scroll_id, paginated results and total of results
        """
        params = {'scroll_id': scroll_id} if scroll_id else {}

        result = self.__class__.management_api_call(
            'get', entry_point='{0}/items/{1}'.format(self.hashid, item_type),
            params = params
        )

        return {'scroll_id': result['response']['scroll_id'],
                'results': result['response']['results'],
                'total': result['response']['count']}


    def process(self):
        """
        Ask the server to process the search engine's feeds

        Returns:
            (True, task_id) The task has been accepted for processing.
                            <task_id> is the id of the accepted task
            (False, None) There is another feed processing going on.
        """
        result = self.__class__.management_api_call(
            'post', entry_point='%s/tasks/process' % self.hashid)

        if result['status_code'] == requests.codes.CREATED:
            return (True, self._obtain_id(result['response']['link']))
        if result['status_code'] == requests.codes.OK:
            return (False, None)

    def process_info(self):
        """
        Obtain info of the last processing task sent to the server

        Returns:
            a dict with the keys 'state' and 'message'
            examples:
            - {'state': 'PROCESSING', 'message': 'Your task is being processed'}
            - {'state': 'SUCCESS', 'message': 'The task has successfuly finished'}
            - {'state': 'FAILURE', 'message': 'no data in the feed'}
        """
        result = self.__class__.management_api_call(
            'get', entry_point='%s/tasks/process' % self.hashid)
        result['response'].pop('task_name', None)

        return result['response']


    def task_info(self, task_id):
        """
        Obtain info about how a task is going or its result

        Returns:
            a dict with the keys 'state', 'message' and 'task_name'
            examples:
            - {'state': 'PROCESSING', 'message': 'Your task is being processed',
               'task_name': 'process'}
            - {'state': 'SUCCESS', 'message': 'The task has successfuly finished',
               'task_name': 'process'}
            - {'state': 'FAILURE', 'message': 'no data in the feed',
               'task_name': 'process'}
        """
        result = self.__class__.management_api_call(
            entry_point='%s/tasks/%s' % (self.hashid, task_id))

        return result['response']

    def logs(self):
        """
        Obtain logs of the latest feed processing tasks done

        Returns:
            (list) list of dicts representing the logs
            example:[{'date': '2013-07-24T12:37:58.990',
                     'level': 'ERROR',
                     'msg': 'Wrong or not existent ...',
                     'log_type': 'log.parser'
                    }, {...}]
        """
        result = self.__class__.management_api_call(
            entry_point='%s/logs' % self.hashid)

        return result['response']

    def query(self, query_term, page=1, filters=None, query_name=None, **kwargs):
        """
        Search the elasticsearch index

        Args:
            query_term:  the actual query
            page: page number
            filters: filter definition.
                Example:
                    {'brand': ['nike', 'addidas'],
                    'price': {'from': 2.34, 'to': 12}}
            query_name: instructs doofinder to use only that query type
            options: dict with additional requests parameters
            any other keyword param is added as request parameter

        Returns:
            A dict representing the response

        Raises:
            NotAllowed: if auth is failed.
            BadRequest: if the request is not proper
            WrongREsponse: if server error
        """
        params = {'hashid': self.hashid, 'query': query_term, 'page': page,
                  filter: filters}
        params.update(kwargs)
        response = self.api_call('search', params)

        return QueryResponse(response['response'])

    def get_options(self):
        """
        Obtain some search engine's options defined at doofinder's control panel.
        Mainly facets

        Returns:
            A dict with the different options
        """
        return self.api_call('options/{0}'.format(self.hashid))['response']

    def _obtain_id(self, url):
        """
        Extracs identifactor from an item or task url .

        Args:
            url: item or task resource locator

        Returns:
            the item or task identificator
        """
        url_re = re.compile('/(?P<hashid>\w{32})/(items/\w+|tasks)/(?P<id>[\w-]+)/?$')

        return url_re.search(url).groupdict()['id']


class Item(dict):
    """
    Simple wrapper to add __getattr__ methods to a dict

    >>> it = Item()
    >>> it
    {}
    >>> it['a'] = 'va'
    >>> it.b = 'vb'
    >>> it
    {'a': 'va', 'b': 'vb'}
    """
    def __init__(self, initial_object=None):
        """prepopulate with initial_object"""
        if type(initial_object) == dict:
            self._hidrate(initial_object)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def _hidrate(self, obj):
        for key, value in obj.iteritems():
            if type(value) == dict:
                value = Item(value)
            if type(value) == list:
                value = map(lambda x: Item(x) if type(x) == dict else x, value)
            self[key] = value


class QueryResponse(Item):
    """
    Wrapper for the json response from a query

    It's just an Item with an extra method
    """
    def get_items(self):
        """return elements from the 'results' list as items"""
        return getattr(self, 'results', [])


class ScrolledItemsIterator(object):
    """ Class to scroll results. i.e. paginate only forward"""

    def __init__(self, search_engine, item_type):
        """
        Args:
            search_engine (SearchEngine): search_engine api management object
            item_type (string): the type of items to scroll
        """
        self.search_engine = search_engine
        self.item_type = item_type
        self._scroll_id = None
        self._position = 0
        self._total = None
        self._results_page = []
        # get first batch of results
        self._fetch_results()

    def _fetch_results(self):
        """Get the next batch of results making an API request"""
        api_results = self.search_engine._get_scrolled_items_page(self.item_type,
                                                                  scroll_id=self._scroll_id)
        self._total = api_results['total']
        self._scroll_id = api_results['scroll_id']
        self._results_page = api_results['results']
        return len(self._results_page)

    def __len__(self):
        return self._total

    def __iter__(self):
        while len(self._results_page):
            for r in self._results_page:
                yield Item(r)
            self._fetch_results()
