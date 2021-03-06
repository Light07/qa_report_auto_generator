# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators, HiddenField, SelectField, \
    SelectMultipleField
from wtforms.validators import Optional

import config

class EFForm(Form):

    qa_resource = StringField(u'QA Resource', [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = StringField(u'Jira Username', [validators.DataRequired("Please input the user name that used for jira login.")])
    password = PasswordField(u'Jira Password', [validators.DataRequired("Please input the password.")])
    project_name = StringField(u'Project Name', [validators.DataRequired("Please input the project name")])
    board_id = IntegerField(u'Board Id', [validators.DataRequired("Please input a integer as board id.")])
    submit = SubmitField(u'Submit')

class SelectFieldForm(Form):

    qa_resource = HiddenField(StringField(u'QA Resource'), [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = HiddenField(StringField(u'Jira Username'), [validators.DataRequired("Please input the user name that used for jira login.")])
    password = HiddenField(PasswordField(u'Jira Password'), [validators.DataRequired("Please input the password.")])
    project_name = HiddenField(StringField(u'Project Name'), [validators.DataRequired("Please input the project name")])
    sprint_name = SelectField(u'Sprint Name', coerce=str)
    board_id = HiddenField(IntegerField(u'Board Id'), [validators.DataRequired("Please input a integer as board id.")])
    submit = SubmitField(u'Submit')

class CustomizedComponentForm(Form):
    qa_resource = HiddenField(StringField(u'QA Resource'), [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = HiddenField(StringField(u'Jira Username'), [validators.DataRequired("Please input the user name that used for jira login.")])
    password = HiddenField(PasswordField(u'Jira Password'), [validators.DataRequired("Please input the password.")])
    project_name = HiddenField(StringField(u'Project Name'), [validators.DataRequired("Please input the project name")])
    sprint_name = SelectField(u'Sprint Name', coerce=str)
    board_id = HiddenField(IntegerField(u'Board Id'), [validators.DataRequired("Please input a integer as board id.")])
    # quick_filter = SelectMultipleField(u'Quick Filter',coerce=str, choices=config.quick_filter_choice)
    quick_filter = SelectField(u'Quick Filter',coerce=str)
    submit = SubmitField(u'Submit')

class SchoolCustomizedForm(Form):
    qa_resource = HiddenField(StringField(u'QA Resource'), [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = HiddenField(StringField(u'Jira Username'), [validators.DataRequired("Please input the user name that used for jira login.")])
    password = HiddenField(PasswordField(u'Jira Password'), [validators.DataRequired("Please input the password.")])
    project_name = SelectMultipleField(u'Select Project',coerce=str, choices=config.school_project_choice)
    submit = SubmitField(u'Submit')
