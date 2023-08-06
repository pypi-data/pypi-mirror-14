#!/usr/bin/env python


class ApiResult(object):
    """
    """
    # status = ""
    # message = ""
    # data = object
    #

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return '<API Results @ Status: {status}>'.format(status=self.status)

    def __repr__(self):
        return '<API Results @ Status: {status}>'.format(status=self.status)

    def __init__(self, json_data):
        #
        if 'operation' in json_data:
            operation = json_data.get('operation')
            api_result = operation.get('result')
            status = api_result.get('status')
            message = api_result.get('message')
            # Yet again ManageEngine shows how bad they are at making a
            # consistant product.
            # - They return what you ask for as Details in some API calls,
            #   and details in others.
            if 'Details' in operation:
                result_data = operation.get('Details')
            elif 'details' in operation:
                result_data = operation.get('details')
        elif 'response_status' in json_data:
            # Be able to handle calls to the v2 API
            status = json_data.get('response_status').get('status')
            message = json_data.get('response_status').get('messages')
            json_data.pop('response_status')
            result_data = json_data
        elif 'GROUP' in json_data:
            # This will make it so a request API call will not fail
            # - This API call does not return a status code or message.
            #   - ManageEngine is bad at standarizing things
            status = 'Success'
            message = (
                'ServiceDesk decided this API call didn\'t need to '
                'return a sucess code')
            result_data = json_data
        else:
            raise Exception(
                'The API call returned something '
                'unexpected!\n\n\n(RESULT: {result})'.format(result=json_data))
        #
        self.__status = status
        self.__message = message
        self.__data = result_data
    #
