from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField, PasswordField, validators


class EFForm(Form):
    qa_resource = StringField(u'qa resource', [validators.DataRequired("Please input the qa who contributed on this sprint.")])
    username = StringField(u'user name', [validators.DataRequired("Please input the user name that used for jira login.")])
    password = PasswordField(u'pass word', [validators.DataRequired("Please input the password.")])
    board_id = IntegerField(u'board id', [validators.DataRequired("Must input a integer.")])
    sprint_name = StringField(u'sprint name', [validators.DataRequired("Please input the sprint name.")])

    submit = SubmitField(u'generate report')