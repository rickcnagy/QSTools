#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""A set of wrappers around different specific REST API's. If the wrapper (or a
part of that wrapper) can be used for another REST API, it should be moved to
rest_base.py
"""

import qs


class GitHubRequest(qs.BaseRequest):
    base_url = 'https://api.github.com'


class HTTPBinRequest(qs.BaseRequest):
    """For test requests at HTTPBin: github.com/kennethreitz/httpbin"""
    base_url = 'https://httpbin.org'


class QSRequest(qs.BaseRequest):
    base_params = {'itemsPerPage': 1000}
    base_url = 'https://api.quickschools.com/sms/v1'

    def __init__(self, description, uri, live=True):
        if not live:
            self.base_url = self.base_url.replace(
                'quickschools',
                'smartschoolcentral')
        self.return_type = None
        self.paging_info = None
        super(QSRequest, self).__init__(description, uri)

    def set_api_key(self, api_key):
        self._api_key = api_key
        self.base_params = qs.merge([{'apiKey': api_key}, self.base_params])

    def _get_data(self):
        if not self.successful: return []

        parsed = self.response.json()
        if 'list' in parsed:
            self.return_type = 'Paged List'
            self.paging_info = {
                'items_per_page': parsed['itemsPerPage'],
                'page': parsed['page'],
                'number_of_pages': parsed['numberOfPages'],
                'number_of_items': parsed['numberOfItems'],
            }
            return parsed['list']
        elif 'id' in parsed:
            self.return_type = 'Single Object'
            return parsed
        elif type(parsed) is list:
            self.return_type = 'Flat List'
            return parsed
        api_logging.critical("Unrecognized response data type", parsed)
