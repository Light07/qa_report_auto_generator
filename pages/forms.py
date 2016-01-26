# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators, HiddenField, SelectField

class EFForm(Form):
    qa_resource = StringField(u'QA Resource', [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = StringField(u'User Name(for jira)', [validators.DataRequired("Please input the user name that used for jira login.")])
    password = PasswordField(u'Password', [validators.DataRequired("Please input the password.")])
    project_name = StringField(u'Project Name', [validators.DataRequired("Please input the project name")])
    board_id = IntegerField(u'Board Id', [validators.DataRequired("Please input a integer as board id.")])
    submit = SubmitField(u'Generate Report')

class SelectFieldForm(Form):
        # qa_resource = StringField(u'qa resource', [validators.DataRequired("Please input the qa who contributed on this sprint.")])
        # username = StringField(u'user name', [validators.DataRequired("Please input the user name that used for jira login.")])
        # password = PasswordField(u'pass word', [validators.DataRequired("Please input the password.")])
        # project_name = StringField(u'project name', [validators.DataRequired("Please input the project name")])
        # sprint_name = SelectField(u'sprint name', coerce=str)
        # board_id = IntegerField(u'board id', [validators.DataRequired("Please input a integer as board id.")])
        # submit = SubmitField(u'generate report')
        qa_resource = HiddenField(StringField(u'QA Resource'), [validators.DataRequired("Please input the qa who contributed on this sprint.")])
        username = HiddenField(StringField(u'User Name(for jira)'), [validators.DataRequired("Please input the user name that used for jira login.")])
        password = HiddenField(PasswordField(u'Password'), [validators.DataRequired("Please input the password.")])
        project_name = HiddenField(StringField(u'Project Name'), [validators.DataRequired("Please input the project name")])
        sprint_name = SelectField(u'Sprint Name', coerce=str)
        board_id = HiddenField(IntegerField(u'Board Id'), [validators.DataRequired("Please input a integer as board id.")])
        submit = SubmitField(u'Generate Report')