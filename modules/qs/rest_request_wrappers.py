#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""A set of wrappers around different specific REST API's. If the wrapper (or a
part of that wrapper) can be used for another REST API, it should be moved to
rest_base.py
"""

import qs


class GitHubRequest(qs.RestRequest):
    base_url = 'https://api.github.com'


class HTTPBinRequest(qs.RestRequest):
    """For test requests at HTTPBin: github.com/kennethreitz/httpbin"""
    base_url = 'https://httpbin.org'


class QSRequest(qs.RestRequest):
    """Requests to the QS REST API on the live server

    Attributes:
        return_type: The return type, such as Flat List, Single Object, etc.
        fields: A list to add to the request in the 'fields' param.
        paging_info: Info extracted for paginated lists on total items, etc.
    """
    base_params = {'itemsPerPage': 1000}
    base_url = 'https://api.quickschools.com/sms/v1'

    def __init__(self, description, uri, **kwargs):
        self.return_type = None
        self.paging_info = None
        self.fields = []

        super(QSRequest, self).__init__(description, uri, **kwargs)

    def _before_request(self):
        if self.fields:
            self.params.update({'fields': ','.join(self.fields)})

    def _get_data(self):
        if not self.successful: return None

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
        elif 'reportCardLevel' in parsed or 'transcriptLevel' in parsed:
            self.return_type = 'Single Object'
            return parsed
        elif type(parsed) is list:
            self.return_type = 'Flat List'
            return parsed
        elif type(parsed) is dict and parsed.keys() == ['success']:
            self.return_type = 'Success Only'
            return parsed

        qs.logger.critical("Unrecognized response data type", parsed)

    def _after_response(self):
        """For now, until QSPaginatedRequest is implemented, exit if more than
        1000 entries are received
        """
        if (self.return_type == 'Paged List'
                and int(self.paging_info['number_of_pages']) > 1):
            qs.logger.critical('Receieved too may responses', self._log_dict())


class QSBackupRequest(QSRequest):
    base_url = 'https://api.smartschoolcentral.com/sms/v1'


class QSLocalRequest(QSRequest):
    base_url = 'http://localhost:8080/sms/v1'
