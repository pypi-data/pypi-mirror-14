#!/usr/bin/env python

import cjson
import requests
import sys
import urllib
from .classes import ApiResult
from .classes import Request
from .classes import Task
from .namedtuples import API_Result
from . import InvalidApiKeyError
from . import InvalidRequestFilterError
from . import InvalidTaskError


class ServiceDesk(object):
    """
    Helper class to handle any communications with servicedesk

    MUST pass the server ServiceDesk lives on as the first option.
    MUST pass an api_key from ServiceDesk as the second option.
    """
    # __host = "example.com"
    # __api_key = "00000000-0000-0000-0000-000000000000"
    # __base_url = "https://{host}/sdpapi"  # Look into moving this into the
    #                                        config file as it may change in
    #                                        an update.
    # __base_request_data = {} - Contains a dict with the base vars that will
    #                            be sent to SD in either a POST or GET request.
    # __request_filters = {'id': 'nice name'} - List of filters the given API
    #                                           key has access to.
    #
    #
    #
    #
    #

    # def get_all_notes(self):
    #     """
    #     """
    #     pass

    # def get_note(self):
    #     """
    #     """
    #     pass

    # def get_worklog(self):
    #     """
    #     """
    #     pass

    # def get_all_worklogs(self):
    #     """
    #     """
    #     pass

    # def get_notes(self):
    #     """
    #     """
    #     pass

    # def get_conversations(self):
    #     """
    #     """
    #     pass

    # def get_request_fields(self):
    #     """
    #     """
    #     pass

    def get_request_filters(self):
        """
        """
        #
        results = self.__apiv1(
            domain='request', operation='GET_REQUEST_FILTERS')

        if not results.status == 'Success':
            raise Exception(
                'Was unable to get a listing of all request filters!')

        raw_data = results.data

        nice_data = {}
        for current_filter in raw_data:
            name = current_filter['VIEWID']
            value = current_filter['VIEWNAME']
            nice_data[name] = value
        return nice_data

    def get_all_requests(self, start_at=0, limit=10, filterby='All_Requests'):
        """
        Returns all requests that match a request filter.
        """
        #
        #
        if filterby not in self.__request_filters.keys():
            raise InvalidRequestFilterError
        #
        #
        # Define the search filter for the API call
        request_filter = {
            'operation': {
                'details': {
                    'from': start_at,
                    'limit': limit,
                    'filterby': filterby,
                },
            },
        }

        # Make the API call asking for all requests that match the filter.
        results = self.__apiv1(
            domain='request',
            operation='GET_REQUESTS',
            input_data=request_filter)

        # Check to see if the API call went through or not.
        if not results.status == 'Success':
            raise Exception(
                'There was an error getting all of the '
                'requests!\n\n\n{result}'.format(result=str(results)))
        resuest_data = results.data
        requests = [
            Request(current_request) for current_request in resuest_data]
        return requests

    def get_all_tasks(
            self, row_count=50, start_index=1, end_index=2,
            fields_required='get_all', sort_column='status',
            sort_order='A', request_id=None, filter='ALL'):
        """
        """
        # Define our search terms
        task_search_data = {
            'list_info': {
                'row_count': str(row_count),
                'start_index': str(start_index),
                'end_index': str(end_index),
                'fields_required': '[{fields}]'.format(fields=fields_required),
                'sort_column': str(sort_column),
                'sort_order': str(sort_order),
            },
            'tasks': {
                'filter': filter,
            },
        }
        # If we are attempting to get tasks for a single request
        if request_id:
            td = task_search_data['tasks']
            td['entity'] = 'request'
            td['associated_entity_id'] = str(request_id)
        api_call_results = self.__apiv2(
            domain='tasks', input_data=task_search_data)
        result_data = api_call_results.data
        #
        if 'tasks' in result_data:
            task_data = api_call_results.data.get('tasks')
            if len(task_data) == 0:
                return []
            tasks = [
                Task(current_task_data)
                for current_task_data in task_data]
            return tasks
        elif 'task' in result_data:
            task_data = result_data.get('task')
            tasks = [Task(task_data[0])]
        return tasks

    def get_task(self, task_id):
        """
        Returns python dict with the details of the given task.
        """
        api_call = self.__apiv2(domain='tasks', domain_object=task_id)
        # Check to make sure the call went through
        if not api_call.status == 'Success':
            raise InvalidTaskError(
                '({task_id}) is not a valid task id!\n\n{message}'.format(
                    task_id=task_id, message=api_call.message))
        # The results of this API call "should" only ever return a single task
        task_data = api_call.data.get('task')[0]
        return Task(input_data=task_data)

    def get_request(self, request_id):
        """
        Return the main information from a request.
        """
        api_results = self.__apiv1(
            domain='request',
            operation='GET_REQUEST',
            domain_object=request_id)
        request = Request(api_results.data)
        return request

    def __apiv1(self, domain, operation, domain_object=None, input_data=None):
        """
        """
        #
        # OPERATION, INPUT_DATA
        # Everything with the V1 API is a POST request
        base_url = self.__base_url
        post_url = '{base}/{domain}'.format(base=base_url, domain=domain)

        # See if we are working with a specfic object inside of an API domain
        # - If we are, make sure we modify the POST url to reflect that
        if domain_object:
            post_url = '{old_base}/{object}'.format(
                old_base=post_url, object=domain_object)

        # Create a copy of the base data which contains format=json and our
        # API key so we can append the OPERATION_NAME to it.
        post_data = self.__base_request_data.copy()
        post_data['OPERATION_NAME'] = operation.upper()

        # If there is any input_data add that to the post_data
        if input_data:
            json_input_data = cjson.encode(input_data)
            post_data['INPUT_DATA'] = json_input_data

        # Make the request to ServiceDesk
        results = self.__communicate(request_url=post_url, data=post_data)

        return ApiResult(json_data=results)

    def __apiv2(
            self, domain, input_data=None, domain_object=None, method='GET'):
        """
        """
        #
        # Create the base request data that each request MUST have
        request_data = self.__base_request_data.copy()

        # If input_data was passed ensure that it gets encoded correctly before
        # we pass it to ServiceDesk.
        if input_data:
            json_input_data = cjson.encode(input_data)
            request_data['INPUT_DATA'] = json_input_data

        # Start to form the url for the request
        base_url = self.__base_url
        request_url = '{base}v2/{domain}'.format(base=base_url, domain=domain)

        # If we are working with a specfic object make sure we append it to
        # the request url.
        if domain_object:
            request_url = '{orig}/{object}'.format(
                orig=request_url, object=domain_object)

        # Create our payload
        post_data = None
        if method == 'GET':
            # Append our request info to the url as we will be doing a GET
            # request
            encoded_data = urllib.urlencode(request_data)
            request_url = '{orig}?{data}'.format(
                orig=request_url, data=encoded_data)
        elif method == 'POST':
            # Store our info as form data as we will be posting
            post_data = request_data
        else:
            raise Excpeiton(
                '({method}) is an unsupported method for the API '
                'v2 function.'.format(method=method))

        results = self.__communicate(request_url=request_url, data=post_data)
        return ApiResult(json_data=results)

    def __communicate(self, request_url, data=None):
        """
        """
        # Determin which type of request should be made
        # - If there is data provided to this function, we must use POST
        if data:
            request = requests.post(url=request_url, data=data)
        else:
            request = requests.get(url=request_url)
        request_data_raw = request.content
        request_data = cjson.decode(request_data_raw)
        return request_data

    def __str__(self):
        return (
            '<ServiceDeskHelper - Host: {host} '
            '- Key: {api_key}>').format(
                host=self.__host,
                api_key='{}-{}'.format(
                    self.__api_key[0:4],
                    self.__api_key[-4:]))

    def __repr__(self):
        return (
            '<ServiceDeskHelper - Host: {host} '
            '- Key: {api_key}>').format(
                host=self.__host,
                api_key='{}-{}'.format(
                    self.__api_key[0:4],
                    self.__api_key[-4:]))

    def __init__(self, host, api_key):
        self.__host = host
        # Define a shortcut for calling the ServiceDesk API
        self.__base_url = 'https://{host}/sdpapi'.format(host=host)
        # TODO: Test to make sure the API Key appears to be valid
        self.__api_key = api_key
        # Define the core of every request that will be sent to the SD API
        self.__base_request_data = {
            'format': 'json',
            'TECHNICIAN_KEY': self.__api_key}
        # Make the helper aware of the filters one is allowed to use.
        # - At the same time we are able to test to make sure the given API
        #   key is valid as the request will fail if the key does not work.
        try:
            self.__request_filters = self.get_request_filters()
        except Exception:
            raise InvalidApiKeyError
        #

if __name__ == "__main__":
    print("Do not run this script directly, it must be imported.")
