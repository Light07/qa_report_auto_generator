__author__ = 'kevin.cai'

import os

jira_options = {'server':"https://jira.englishtown.com"}#, 'verify': False}

jira_account = {'username':"kevin.cai", 'password':"***"}

# Project Key
project_name = None

board_id = None

# For engage team, ATEAM, customized usage
p_name = {"Engage": "ME", "ATEAM":"ATEAM"}
b_id = {"Engage":"416", "ATEAM":"60"}

# For School team, customized usage
s_name = "SPC, SD"
s_dict = {"SPC":128 , "SD":42}
school_project_choice = [('SPC', 'SPC'), ('SD', 'SD')]

# Components filter.
show_all = "Show All"
show_all_but_exclude_those_have_components = "Show All but exclude above"
quick_filter_choice = {"ME":[('iOS', 'iOS'), ('Android', 'Android'), \
                             (show_all_but_exclude_those_have_components, show_all_but_exclude_those_have_components), (show_all, show_all)],\
                       "ATEAM":[('EVCMobile', 'EVCMobile'), \
                                (show_all_but_exclude_those_have_components, show_all_but_exclude_those_have_components), (show_all, show_all)]}

# Used to control how many sprint will shown on index page.
num_of_sprint_shown = 10

sprint_name = None

qa_resource = None

# After confirmed with Scrum master, we usually close story days after it finished, hence use this value as a  buffer configuration
delay_day = 4

# Used for flask as secret key
secrt_key = os.urandom(32)