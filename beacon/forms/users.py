# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from beacon.models.users import Department

class DepartmentForm(Form):
    '''Allows user to update profile information

    Attributes:
        department: sets user department based on choice of available
            departments or none value
        first_name: sets first_name value based on user input
        last_name: sets last_name value based on user input
    '''
    department = QuerySelectField(
        query_factory=Department.query_factory,
        get_pk=lambda i: i.id,
        get_label=lambda i: i.name,
        allow_blank=True, blank_text='-----'
    )
    first_name = TextField()
    last_name = TextField()
