__author__ = 'kevin.cai'

jira_options = {'server':"https://jira.englishtown.com"}

jira_account = {'username':"kevin.cai", 'password':"***"}

# Project Key
project_name = None

board_id = None


# For engage team, customized usage
p_name = "ME"
b_id = "416"
quick_filter_choice = [('iOS', 'iOS'), ('Android', 'Android'), ('-1','Plese select a component')]

# Used to control how many sprint will shown on index page.
num_of_sprint_shown = 10

sprint_name = None

qa_resource = None

# After confirmed with Scrum master, we usually close story days after it finished, hence use this value as a  buffer configuration
delay_day = 4

# Used for flask as secret key
secrt_key = "EF Sprint Report"