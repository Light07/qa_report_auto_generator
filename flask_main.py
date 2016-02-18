# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, render_template, flash, session, make_response

import config
from pages.jira_helper import JiraHelper
from pages.forms import EFForm, SelectFieldForm, EngageCustomizedForm

app = Flask(__name__)
app.secret_key = config.secrt_key
response = None
quick_filter = None

@app.route('/', methods=["GET", "POST"])
def index():
    form = EFForm()
    if request.method== "POST" :
        if form.submit.data and form.validate():
            session['qa_resource'] = form.qa_resource.data
            session['username'] = form.username.data
            session['password'] = form.password.data
            session['board_id'] = form.board_id.data
            session['project_name'] = form.project_name.data

            # Update config value for class JiraHelper use.
            config.jira_account['username'] = session['username']
            config.jira_account['password'] = session['password']
            config.board_id = session['board_id']
            config.qa_resource =session['qa_resource']
            config.project_name = session['project_name']

            # Return 10 sprint based on given board id
            jira = JiraHelper(config.jira_options, config.jira_account)
            sprint_choice = jira.get_num_of_sprint_names_by_board_id(int(form.board_id.data))
            sprint_choice.append(('-1', 'Please select a sprint'))
            session['sprint_name'] = sprint_choice

            if request.form.get('project_name') in config.p_name and request.form.get('board_id') in config.b_id:
                return redirect(url_for('customized_component_index'))

            return redirect(url_for('get_sprint_list'))
        else:
            flash('All fields are required.')
            return render_template('index.html', form=form)

        return render_template('index.html',form=form)

    elif request.method == 'GET':
        return  render_template('index.html',form=form)

@app.route('/customized_component_index', methods=["GET", "POST"])
def customized_component_index():
    form = EngageCustomizedForm()
    form.qa_resource.data = session['qa_resource']
    form.username.data = session['username']
    form.password.data =  session['password']
    form.board_id.data = session['board_id']
    form.project_name.data =session['project_name']
    form.sprint_name.choices= session['sprint_name']

    if request.method== "POST" :
        if form.submit.data and form.validate():
            global quick_filter
            quick_filter = form.quick_filter.data
            session["choice_sprint"] = form.sprint_name.data

            return redirect(url_for('get_report'))
        else:
            flash('All fields are required.')
            return render_template('customized_component_index.html', form=form)

    elif request.method == "GET":
        return render_template('customized_component_index.html', form=form)

    return  render_template('customized_component_index.html', form=form)


@app.route('/sprint', methods=["GET", "POST"])
def get_sprint_list():
    form=SelectFieldForm()
    form.qa_resource.data = session['qa_resource']
    form.username.data = session['username']
    form.password.data =  session['password']
    form.board_id.data = session['board_id']
    form.project_name.data =session['project_name']
    form.sprint_name.choices= session['sprint_name']

    if request.method== "POST" :
        if form.submit.data and form.validate():
            session["choice_sprint"] = form.sprint_name.data

            return redirect(url_for('get_report'))
        else:
            flash('All fields are required.')
            return render_template('show_sprint_lists.html', form=form)

    elif request.method == "GET":
        return render_template('show_sprint_lists.html', form=form)

    return  render_template('show_sprint_lists.html', form=form)

@app.route('/success')
def success():
    global response
    response.headers["Content-Disposition"] = "attachment; filename=Sprint_Report.html"
    request.headers.get('User-Agent')
    return response


@app.route('/report', methods=["GET"])
def get_report():
    config.jira_account['username'] = str(session['username'])
    config.jira_account['password'] = str(session['password'])

    jira = JiraHelper(config.jira_options, config.jira_account)

    config.board_id = str(session.get('board_id'))

    config.sprint_name = session['choice_sprint']

    config.qa_resource = str(session['qa_resource'])

    config.project_name = str(session['project_name'])

    sprint_id = jira.get_sprint_id_by_sprint_name(int(config.board_id), config.sprint_name)

    sprint_status = jira.html_get_sprint_status(sprint_id, config.board_id)
    global quick_filter
    if quick_filter:

        standard_task_id_list = jira.get_standard_tasks_id_by_sprint(sprint_id, config.project_name)
        standard_task_id_list = jira.get_filtered_task_id_by_component(standard_task_id_list, quick_filter)
        #
        standard_tasks_info_by_sprint = jira.get_standard_tasks_info_by_sprint(sprint_id, config.project_name)
        standard_tasks_info_by_sprint = jira.get_filtered_task_info_by_component(standard_tasks_info_by_sprint, quick_filter)
        #
        raw_bug_id_list = jira.get_bug_id_by_sprint(sprint_id, config.board_id, config.project_name)
        raw_bug_id_list = jira.get_filtered_task_id_by_component(raw_bug_id_list, quick_filter)
        #
        raw_bug_list = jira.get_bug_info_by_sprint(sprint_id, config.board_id, config.project_name)
        raw_bug_list = jira.get_filtered_task_info_by_component(raw_bug_list, quick_filter)
        #
        change_request_id_list = jira.get_change_request_id_by_sprint(sprint_id, config.project_name)
        change_request_id_list = jira.get_filtered_task_id_by_component(change_request_id_list, quick_filter)
        #
        raw_live_defect_id_list = jira.get_live_defect_id_by_sprint(sprint_id, config.project_name)
        raw_live_defect_id_list = jira.get_filtered_task_id_by_component(raw_live_defect_id_list, quick_filter)
        #
        raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id, config.project_name)
        raw_live_defect_list = jira.get_filtered_task_info_by_component(raw_live_defect_list, quick_filter)
        #
        bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id, config.board_id, config.project_name)
        bugs_opened_before_but_closed_in_sprint = jira.get_filtered_task_info_by_component(bugs_opened_before_but_closed_in_sprint, quick_filter)
        #
        raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id, config.board_id, config.project_name)
        raw_automation_bug_list = jira.get_filtered_task_info_by_component(raw_automation_bug_list, quick_filter)
        #
        raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id, config.project_name)
        raw_change_request_list = jira.get_filtered_task_info_by_component(raw_change_request_list, quick_filter)
        #
        bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id, config.board_id, config.project_name, quick_filter)
    else:

        standard_task_id_list = jira.get_standard_tasks_id_by_sprint(sprint_id, config.project_name)
        standard_tasks_info_by_sprint = jira.get_standard_tasks_info_by_sprint(sprint_id, config.project_name)
        #
        raw_bug_id_list = jira.get_bug_id_by_sprint(sprint_id, config.board_id, config.project_name)
        raw_bug_list = jira.get_bug_info_by_sprint(sprint_id, config.board_id, config.project_name)
        #
        change_request_id_list = jira.get_change_request_id_by_sprint(sprint_id, config.project_name)
        #
        raw_live_defect_id_list = jira.get_live_defect_id_by_sprint(sprint_id, config.project_name)
        #
        raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id, config.project_name)

        bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id, config.board_id, config.project_name)
        #
        raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id, config.board_id, config.project_name)
        #
        raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id, config.project_name)
        #
        bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id, config.board_id, config.project_name)

    actual_points = jira.get_actual_story_points_by_sprint(standard_tasks_info_by_sprint)

    sprint_bug_nested_list = jira.html_get_bug_list_by_tasks(raw_bug_list)

    previous_bugs_closed_in_sprint = jira.html_get_bug_list_by_tasks(bugs_opened_before_but_closed_in_sprint)

    sprint_automation_bug_list = jira.html_get_bug_list_by_tasks(raw_automation_bug_list)
    sprint_automation_bug_percentage = jira.html_get_automation_found_bug_percentange(raw_bug_id_list, raw_automation_bug_list)

    sprint_live_defect_nested_list = jira.html_get_bug_list_by_tasks(raw_live_defect_list)
    sprint_live_defect_percentage = jira.html_get_live_defect_percentage_of_all_defects(raw_live_defect_id_list, raw_bug_id_list )


    sprint_change_request_nested_list = jira.html_get_bug_list_by_tasks(raw_change_request_list)
    sprint_change_request_percentage = jira.html_get_change_request_percentage_of_all_defects(standard_task_id_list, change_request_id_list)

    #
    bug_priority_list = jira.html_get_share_ratio_by_priority(raw_bug_list)
    bug_priority_detail = jira.html_get_share_ratio_detail_by_priority(raw_bug_list)

    #
    story_list= jira.get_task_id_that_has_linked_task(raw_bug_id_list)
    story_share = jira.html_get_linked_issue_num_group_by_story(story_list)
    story_share_detail = jira.html_get_linked_issue_detail_group_by_story(story_list, raw_bug_id_list)[1]

    render = render_template('sprint_report.html', project_required=config.project_name, \
                             customized_component=quick_filter, \
                             sprint_name_string=config.sprint_name,\
                            qa_resource = config.qa_resource,\
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
    global response
    response = make_response(render)

    quick_filter = None

    return render

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", debug=False, threaded=True)

