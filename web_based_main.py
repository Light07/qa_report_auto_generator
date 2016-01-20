# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, \
    render_template, flash, session

import settings
from pages.forms import EFForm
from pages.jira_helper import JiraHelper

app = Flask(__name__)

app.config['SECRET_KEY'] = 'EF Sprint Report'

@app.route('/', methods=["GET", "POST"])
def index():
    form = EFForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('index.html', form=form)
        else:
            session['qa_resource'] = form.qa_resource.data
            session['username'] = form.username.data
            session['password'] = form.password.data
            session['board_id'] = form.board_id.data
            session['sprint_name'] = form.sprint_name.data
            return redirect(url_for('get_report'))

    elif request.method == 'GET':
        return render_template('index.html', form=form)

@app.route('/report', methods=["GET"])
def get_report():

    jira_account = {}
    jira_account['username'] = str(session['username'])
    jira_account['password'] = str(session['password'])

    jira = JiraHelper(settings.jira_options, jira_account)

    board_id = str(session['board_id'])
    sprint_name = str(session['sprint_name'])
    qa_resource = str(session['qa_resource'])

    sprint_id = jira.get_sprint_id_by_sprint_name(int(board_id), sprint_name)

    sprint_status = jira.html_get_sprint_status(sprint_id)

    actual_points = jira.html_get_actual_story_points_by_sprint(sprint_id)

    #
    raw_bug_list =jira.get_bug_info_by_sprint(sprint_id)
    sprint_bug_nested_list = jira.html_get_bug_list_by_tasks(raw_bug_list)

    #
    bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id)
    previous_bugs_closed_in_sprint = jira.html_get_bug_list_by_tasks(bugs_opened_before_but_closed_in_sprint)

    #
    raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id)
    sprint_automation_bug_list = jira.html_get_bug_list_by_tasks(raw_automation_bug_list)
    sprint_automation_bug_percentage = jira.html_get_automation_found_bug_percentange(sprint_id)

    #
    raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id)
    sprint_live_defect_nested_list = jira.html_get_bug_list_by_tasks(raw_live_defect_list)
    sprint_live_defect_percentage = jira.html_get_live_defect_percentage_of_all_defects(sprint_id)

    #
    raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id)
    sprint_change_request_nested_list = jira.html_get_bug_list_by_tasks(raw_change_request_list)
    sprint_change_request_percentage = jira.html_get_change_request_percentage_of_all_defects(sprint_id)

    #
    bug_priority_list = jira.html_get_share_ratio_by_priority(sprint_id)
    bug_priority_detail = jira.html_get_share_ratio_detail_by_priority(sprint_id)

    #
    story_list= jira.get_task_id_that_has_linked_task(sprint_id)
    story_share = jira.html_get_linked_issue_num_group_by_story(story_list)
    story_share_detail = jira.html_get_linked_issue_detail_group_by_story(sprint_id, story_list)

    #
    bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id)

    return render_template('sprint_report.html', sprint_name_string=sprint_name,\
                            qa_resource = qa_resource,\
                            sprint_status=sprint_status, actual_story_points=actual_points, \
                            sprint_bug_nested_lists=sprint_bug_nested_list,\
                            bug_priority_nested_lists=bug_priority_list, \
                            bug_priority_share_detail_info=bug_priority_detail,\
                            story_share_nested_lists=story_share, \
                            story_share_detail_info=story_share_detail,\
                            total_bug_and_opened_bug_pair_nested_list=bug_trends,\
                            sprint_automation_found_bug_nested_lists=sprint_automation_bug_list, \
                            sprint_automation_bug_percentage=sprint_automation_bug_percentage,\
                            previous_bugs_closed_in_sprint = previous_bugs_closed_in_sprint,
                            sprint_live_defect_nested_lists=sprint_live_defect_nested_list,\
                            sprint_live_defect_percentage=sprint_live_defect_percentage,\
                            sprint_change_request_nested_lists=sprint_change_request_nested_list, \
                            sprint_change_request_percentage=sprint_change_request_percentage)

if __name__ == '__main__':
    app.run(debug=False)





