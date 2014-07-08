#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import math
import requests
import api_logging
import time

base_uri = 'https://api.pipelinedeals.com/api/v3'
api_key = ''

# use these when specifying PLDRequest functions
DELETE = requests.delete
GET = requests.get
PUT = requests.put
POST = requests.post

# =============================
# = Convenience API Functions =
# =============================


def update_company(company, data, critical=False):
    """data should be like {'company[name]':'Python'}"""
    r = PLDRequest(
        "PUT company data",
        "/companies/{}.json".format(company['id']))
    r.request_data = data
    r.function = PUT
    r.critical = critical
    r.make_request()
    return r.data


def update_deal(deal, data):
    r = PLDRequest(
        "PUT deal data",
        "/deals/{}.json".format(deal['id'])
        )
    r.request_data = data
    r.function = PUT
    r.critical = True
    r.make_request()
    return r.data


def create_person(company_id, user_id, first_name='Default', last_name='Contact'):
    r = PLDRequest('POST person', '/people.json')
    r.params = {
        'person[first_name]': first_name,
        'person[last_name]': last_name,
        'person[company_id]': company_id,
        'person[type]': 'Lead',
        'person[user_id]': user_id
    }
    r.function = POST
    r.critical = False
    # api_logging.info("would put", r.params)
    r.make_request()
    return r.data


def update_person(person, data):
    r = PLDRequest('PUT person', '/people/{}.json'.format(person['id']))
    r.params = {
        'deliver_reassignment_email': False
    }
    r.function = PUT
    r.request_data = data
    r.critical = True
    r.make_request()
    return r.data


def get_companies(parameters=None):
    r = PaginatedPLDRequest("GET companies", '/companies.json')
    if parameters:
        r.params = parameters
    r.make_request()
    return r


def get_company(company_id):
    r = PLDRequest("GET company", '/companies/{}.json'.format(company_id))
    r.critical = True
    r.make_request()
    return r.data

def get_deal(deal_id):
    r = PLDRequest("GET deal", '/deals/{}.json'.format(deal_id))
    r.critical = True
    r.make_request()
    return r.data

def get_deals(filter=None):
    r = PLDRequest("GET filtered deals", '/deals.json')
    if filter:
        r.params = filter
    r.make_request()
    return r.data['entries']


def add_note_to_company(company, content, category_id):
    """want to set company_id, user_id, note_category_id, content"""
    r = PLDRequest("POST company notes", '/notes.json')
    r.critical = True
    r.request_data = {
        'note[content]': content,
        'note[note_category_id]': category_id,
        'note[company_id]': company['id'],
    }
    r.function = POST
    r.make_request()
    return r.data


# ===========================================
# = Functions for interacting with PLD data =
# ===========================================


def custom_field_key(label):
    return 'company[custom_fields][custom_label_{}]'.format(label)

# ===========
# = Classes =
# ===========


class PLDRequest(object):

    def __init__(self, description, uri):
        self.description = description
        self.uri = uri
        self.function = GET
        self.params = {}
        self.request_data = {}
        self.critical = False
        self.silent = False
        self.response = None
        self.text = None
        self.json = None
        self.data = None

    def make_request(self):
        self.log_before()
        self.response = self.function(
            self.full_uri(), params=self.full_params(), data=self.request_data)
        self.text = self.response.text
        try:
            self.json = self.response.json()
        except ValueError:
            self.json = self.text
        self.process_response()
        self.log_after()
        return self

    def process_response(self):
        self.data = self.json

    def log_before(self):
        if not self.silent:
            params = {
                'params': self.full_params(),
                'function': str(self.function),
                'uri': self.uri,
                'full_uri': self.full_uri(),
            }
            if self.request_data:
                params['data'] = self.request_data
            api_logging.info(
                self.description, params, is_request=True)

    def log_after(self):
        if not self.silent:
            data = {
                'response': self.json,
                'http status code': self.response.status_code
                }
            if self.success():
                api_logging.info(self.description, data, is_response=True)
            else:
                api_logging.error_or_critical(
                    self.description, data, self.critical, is_response=True)

    def full_params(self):
        basic_param = {'api_key': api_key}
        return self.merge(basic_param, self.params)

    def full_uri(self):
        return base_uri + self.uri

    def success(self):
        return self.response.status_code == 200

    def merge(self, dict1, dict2):
        return dict(dict1.items() + dict2.items())


class PaginatedPLDRequest(PLDRequest):

    def __init__(self, description, uri):
        super(PaginatedPLDRequest, self).__init__(description, uri)
        self.pagination = None
        self.per_page = None
        self.total_entries = 0
        self.total_pages = 0
        self.all_data = []
        self.start_time = None
        self._current_datum = None

        self.current_page = 1
        self.current_entry = 1

    def full_params(self):
        basic_param = {'page': self.current_page}
        return dict(
            super(PaginatedPLDRequest, self).full_params().items()
            + basic_param.items()
            )

    def process_response(self):
        super(PaginatedPLDRequest, self).process_response()
        if not self.start_time:
            self.start_time = time.time()

        self.pagination = self.json['pagination']
        self.per_page = self.pagination['per_page']
        self.total_entries = self.pagination['total']
        self.total_pages = math.ceil(float(self.total_entries) / self.per_page)
        self.data = self.json['entries']

    def get_all(self, stop_condition=lambda x: False):
        """this should be used when the list will be changing AS you're paging
        stop_when_true terminates if a value doesn't return true
        """
        while(self.has_next()):
            if stop_condition(self.next()): break
            self.all_data.append(self._current_datum)
        return self.all_data

    def has_next(self):
        return self.has_next_on_page() or self.has_next_page()

    def next(self):
        next_entry = None
        if not self.has_next_on_page() and self.has_next_page():
            self.get_next_page()
        if self.has_next_on_page():
            self._current_datum = self.data[self.current_entry - 1]
            self.current_entry += 1
        return self._current_datum

    def has_next_entry(self):
        return (self.current_entry - 1) < len(self.data)

    def has_next_on_page(self):
        return (self.current_entry <= self.per_page and self.has_next_entry())

    def has_next_page(self):
        return self.current_page < self.total_pages

    def get_next_page(self):
        self.current_page += 1
        self.current_entry = 1
        self.make_request()

    def absolute_index(self):
        """index from overall list, not current page"""
        return self.current_entry + (self.current_page - 1) * self.per_page - 1
