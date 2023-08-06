#!/usr/bin/env python

import collections


class Task(object):
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
            if self.__raw.get(name)
            else None
            for current_element in elements]
        return NT(*data)

    @property
    def actual_endtime(self):
        return self.__raw.get('actual_endtime')

    @property
    def actual_starttime(self):
        return self.__raw.get('actual_starttime')

    @property
    def additional_cost(self):
        return self.__raw.get('additional_cost')

    @property
    def associated_entity_id(self):
        return self.__raw.get('associated_entity_id')

    @property
    def comment(self):
        return self.__raw.get('comment')

    @property
    def created_by(self):
        return self.__generic_named_tuple_return(
            name='created_by', elements=['id', 'name'])

    @property
    def created_date(self):
        return self.__generic_named_tuple_return(
            name='created_date', elements=['value', 'display_value'])

    @property
    def description(self):
        return self.__raw.get('description')

    @property
    def entity(self):
        return self.__raw.get('entity')

    @property
    def estimated_effort_days(self):
        return self.__raw.get('estimated_effort_days')

    @property
    def estimated_effort_hours(self):
        return self.__raw.get('estimated_effort_hours')

    @property
    def estimated_effort_minutes(self):
        return self.__raw.get('estimated_effort_minutes')

    @property
    def group(self):
        return self.__generic_named_tuple_return(
            name='group', elements=['id', 'name'])

    @property
    def marked_group(self):
        return self.__raw.get('marked_group')

    @property
    def marked_owner(self):
        return self.__raw.get('marked_owner')

    @property
    def milestoneid(self):
        return self.__raw.get('milestoneid')

    @property
    def owner(self):
        return self.__generic_named_tuple_return(
            name='owner', elements=['id', 'name'])

    @property
    def percentage_completion(self):
        return self.__raw.get('percentage_completion')

    @property
    def priority(self):
        return self.__generic_named_tuple_return(
            name='priority', elements=['id', 'name'])

    @property
    def projectid(self):
        return self.__raw.get('projectid')

    @property
    def scheduled_endtime(self):
        return self.__raw.get('scheduled_endtime')

    @property
    def scheduled_starttime(self):
        return self.__raw.get('scheduled_starttime')

    @property
    def status(self):
        return self.__generic_named_tuple_return(
            name='status', elements=['id', 'name'])

    @property
    def task_id(self):
        return self.__raw.get('task_id')

    @property
    def task_type(self):
        return self.__raw.get('task_type')

    @property
    def title(self):
        return self.__raw.get('title')

    def __repr__(self):
        return (
            '<Task @ ID: {task_id} - Title: {title} - '
            'Priority: {priority}>').format(
                task_id=self.task_id, title=self.title, priority=self.priority)

    def __str__(self):
        return (
            '<Task @ ID: {task_id} - Title: {title} - '
            'Priority: {priority}>').format(
                task_id=self.task_id, title=self.title, priority=self.priority)

    def __init__(self, input_data):
        self.__raw = input_data
