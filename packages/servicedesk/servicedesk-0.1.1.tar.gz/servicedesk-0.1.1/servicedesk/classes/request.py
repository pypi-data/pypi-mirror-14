#!/usr/bin/env python

import collections


class Request(object):
    """
    """

    def __generate_named_tuple(self, name, elements=[]):
        """
        Creates a namedtuple object.
        """
        return collections.namedtuple(name, elements)

    def __generic_named_tuple_return(self, name, elements):
        NT = self.__generate_named_tuple(name=name, elements=elements)
        data = [
            self.__raw.get(name).get(current_element)
            for current_element in elements]
        return NT(*data)

    @property
    def category(self):
        return self.__raw.get('CATEGORY')

    @property
    def closurecode(self):
        return self.__raw.get('CLOSURECODE')

    @property
    def closurecomments(self):
        return self.__raw.get('CLOSURECOMMENTS')

    @property
    def completedtime(self):
        return self.__raw.get('COMPLETEDTIME')

    @property
    def createdby(self):
        return self.__raw.get('CREATEDBY')

    @property
    def createdtime(self):
        return self.__raw.get('CREATEDTIME')

    @property
    def department(self):
        return self.__raw.get('DEPARTMENT')

    @property
    def description(self):
        return self.__raw.get('DESCRIPTION')

    @property
    def duebytime(self):
        return self.__raw.get('DUEBYTIME')

    @property
    def group(self):
        return self.__raw.get('GROUP')

    @property
    def impact(self):
        return self.__raw.get('IMPACT')

    @property
    def impactdetails(self):
        return self.__raw.get('IMPACTDETAILS')

    @property
    def isvipuser(self):
        return self.__raw.get('ISVIPUSER')

    @property
    def item(self):
        return self.__raw.get('ITEM')

    @property
    def mode(self):
        return self.__raw.get('MODE')

    @property
    def priority(self):
        return self.__raw.get('PRIORITY')

    @property
    def requester(self):
        return self.__raw.get('REQUESTER')

    @property
    def requesttype(self):
        return self.__raw.get('REQUESTTYPE')

    @property
    def resolvedtime(self):
        return self.__raw.get('RESOLVEDTIME')

    @property
    def respondedtime(self):
        return self.__raw.get('RESPONDEDTIME')

    @property
    def shortdescription(self):
        return self.__raw.get('SHORTDESCRIPTION')

    @property
    def site(self):
        return self.__raw.get('SITE')

    @property
    def status(self):
        return self.__raw.get('STATUS')

    @property
    def subcategory(self):
        return self.__raw.get('SUBCATEGORY')

    @property
    def subject(self):
        return self.__raw.get('SUBJECT')

    @property
    def technician(self):
        return self.__raw.get('TECHNICIAN')

    @property
    def technician_loginname(self):
        return self.__raw.get('TECHNICIAN_LOGINNAME')

    @property
    def timespentonreq(self):
        return self.__raw.get('TIMESPENTONREQ')

    @property
    def urgency(self):
        return self.__raw.get('URGENCY')

    @property
    def workorderid(self):
        return self.__raw.get('WORKORDERID')

    @property
    def yettoreplycount(self):
        return self.__raw.get('YETTOREPLYCOUNT')

    def __str__(self):
        return (
            '<Request @ ID: {id} - Priority: {priority} - '
            'Title: {title}>').format(
                id=self.workorderid,
                priority=self.priority,
                title=self.subject)

    def __repr__(self):
        return (
            '<Request @ ID: {id} - Priority: {priority} - '
            'Title: {title}>').format(
                id=self.workorderid,
                priority=self.priority,
                title=self.subject)

    def __init__(self, request_data):
        self.__raw = request_data
