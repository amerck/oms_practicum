import requests
from requests.auth import HTTPBasicAuth


class ServiceNowClient:

    def __init__(self, base_url, username, password):
        """
        Initialize a ServiceNow client instance.

        :param base_url: The base URL of the ServiceNow instance.
        :param username: ServiceNow username
        :param password: ServiceNow password
        """
        auth = HTTPBasicAuth(username, password)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = auth
        self.session.headers.update(headers)


    def get_task_by_number(self, number):
        """
        Get a TASK ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/sc_task'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_archived_task_by_number(self, number):
        """
        Get an archived TASK ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/ar_sc_task'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_incident_by_number(self, number):
        """
        Get an INC ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/incident'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_archived_incident_by_number(self, number):
        """
        Get an archived INC ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/ar_incident'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_request_by_number(self, number):
        """
        Get a RITM ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/sc_req_item'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_archived_request_by_number(self, number):
        """
        Get an archived RITM ticket record by its number.

        :param number: ticket number
        :return: result dictionary
        """
        url = self.base_url + '/api/now/table/ar_sc_req_item'
        params = {'sysparm_query': 'number=%s' % number,
                  'sysparm_display_value': 'true'}
        r = self.session.get(url, params=params)
        return r.json()


    def get_ticket_by_number(self, number):
        """
        Get a ticket record by its number.
        Queries TASK, INC, and RITM API endpoints.

        :param number: ticket number
        :return: ticket dictionary
        """
        if number.startswith('TASK'):
            r = self.get_task_by_number(number)
            if not r.get('result'):
                r = self.get_archived_task_by_number(number)
        elif number.startswith('INC'):
            r = self.get_incident_by_number(number)
            if not r.get('result'):
                r = self.get_archived_incident_by_number(number)
        elif number.startswith('RITM'):
            r = self.get_request_by_number(number)
            if not r.get('result'):
                r = self.get_archived_request_by_number(number)
        else:
            r = dict()

        result = r.get('result')
        if not result:
            return dict()
        return result[0]
