# -*- coding: utf-8 -*-

from directory.exceptions import DirectoryValidationException
from directory.scraper import get_search_inputs, get_results
from directory.helpers import (search_button_aliases,
                               search_field_aliases,
                               valid_department,
                               valid_person_type,
                               search_field_full_name)


class Search(object):
    def __init__(self, query='', last_name='', first_name='', email='',
                 phone='', address='', location='', job_title='',
                 person_type='', department=''):
        self.query = query
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
        self.phone = phone
        self.address = address
        self.location = location
        self.job_title = job_title
        self.person_type = person_type
        self.department = department

    def validate(self):
        for field in self.__dict__:
            if field not in search_field_aliases:
                raise DirectoryValidationException('"{}" not a valid field'
                                                   .format(field))

        if not valid_department(self.department):
            raise DirectoryValidationException('"{}" not a valid department'
                                               .format(self.department))

        if not valid_person_type(self.person_type):
            raise DirectoryValidationException('"{}" not a valid person type'
                                               .format(self.person_type))

        if self.query and len([v for v in self.__dict__.values() if v]) > 1:
            raise DirectoryValidationException('Cannot set both query and'
                                               'advanced search params.')

    def search_fields(self):
        search_fields = get_search_inputs()
        full_field_names = search_fields.keys()

        for field in self.__dict__.keys():
            key = search_field_full_name(full_field_names, field)
            search_fields[key] = self.__dict__[field]

        if self.query:
            del search_fields[search_button_aliases['advanced']]

        return search_fields

    def results(self):
        self.validate()
        return get_results(self.search_fields())
