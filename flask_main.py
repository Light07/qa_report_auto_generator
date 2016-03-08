# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, flash, session, make_response, jsonify

import config
from pages.jira_helper import JiraHelper
from pages.forms import EFForm, SelectFieldForm, EngageCustomizedForm, SchoolCustomizedForm

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
            session['project_name'] = (form.project_name.data).upper()

            # Update config value for class JiraHelper use.
            jira_account = {}
            jira_account['username'] = session['username']
            jira_account['password'] = session['password']

            for item in request.form.get('project_name'):
                if item.upper().strip() in config.s_name:
                    return redirect(url_for('school_customized_index'))

            # Return 10 sprint based on given board id
            jira = JiraHelper(config.jira_options, jira_account)
            sprint_choice = jira.html_get_num_of_sprint_names_by_board_id(int(form.board_id.data))
            sprint_choice.append(('-1', 'Please select a sprint'))
            session['sprint_name'] = sprint_choice

            if (request.form.get('project_name')).upper() in config.p_name and request.form.get('board_id') in config.b_id:
                return redirect(url_for('engage_customized_index'))

            return redirect(url_for('get_sprint_list'))
        else:
            flash('All fields are required.')
            return render_template('index.html', form=form)

        return render_template('index.html',form=form)

    elif request.method == 'GET':
        return  render_template('index.html',form=form)

@app.route('/engage_customized_index', methods=["GET", "POST"])
def engage_customized_index():
    form = EngageCustomizedForm()
    form.qa_resource.data = session['qa_resource']
    form.username.data = session['username']
    form.password.data = session['password']
    form.board_id.data = session['board_id']
    form.project_name.data =session['project_name']
    form.sprint_name.choices= session['sprint_name']

    if request.method== "POST" :
        if form.submit.data and form.validate():
            if form.quick_filter.data != "Show All":
                session["quick_filter"] = form.quick_filter.data
            session["choice_sprint"] = form.sprint_name.data

            return redirect(url_for('get_report'))
        else:
            flash('All fields are required.')
            return render_template('engage_customized_index.html', form=form)

    elif request.method == "GET":
        return render_template('engage_customized_index.html', form=form)

    return render_template('engage_customized_index.html', form=form)

@app.route('/school_customized_index', methods=["GET", "POST"])
def school_customized_index():

    form = SchoolCustomizedForm()
    form.qa_resource.data = session['qa_resource']
    form.username.data = session['username']
    form.password.data = session['password']

    jira_account = {}
    jira_account['username'] = session['username']
    jira_account['password'] = session['password']
    jira = JiraHelper(config.jira_options, jira_account)

    if request.method == "POST" :
        if form.submit.data and form.validate():
            project = request.form.getlist("check")
            session['project_name'] = project

            sprint_choice = []
            html_sprint_choice = []
            if len(project) > 0:
                for p in project:
                    session["board_id"] = config.s_dict[p.upper()]
                    # Return 10 sprint based on given board id
                    temp_sprint_choice = jira.get_num_of_sprint_names_by_board_id(config.s_dict[p.upper()])
                    for l in temp_sprint_choice:
                        if l not in sprint_choice:
                            sprint_choice.append(l)
                for l in sprint_choice:
                    html_sprint_choice.append((l, l))

                html_sprint_choice.append(('-1', 'Please select a sprint'))
                session['sprint_name'] = html_sprint_choice
                return redirect(url_for('get_sprint_list'))
            else:
                return render_template('school_customized_index.html', form=form)
        else:

            return render_template('school_customized_index.html', form=form)

    elif request.method == "GET":
        return render_template('school_customized_index.html', form=form)

    return render_template('school_customized_index.html', form=form)

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
    project_name = session['project_name']
    if type(project_name) is list:
        return redirect(url_for('get_school_report'))

    jira_account = {}
    jira_account['username'] = str(session['username'])
    jira_account['password'] = str(session['password'])

    jira = JiraHelper(config.jira_options, jira_account)

    board_id = str(session.get('board_id'))

    sprint_name = session['choice_sprint']

    qa = str(session['qa_resource'])

    sprint_id = jira.get_sprint_id_by_sprint_name(int(board_id), sprint_name)

    sprint_status = jira.html_get_sprint_status(sprint_id, board_id)

    if "quick_filter" in session:

        standard_task_id_list = jira.get_standard_tasks_id_by_sprint(sprint_id, project_name)
        standard_task_id_list = jira.get_filtered_task_id_by_component(standard_task_id_list, session["quick_filter"])
        #
        standard_tasks_info_by_sprint = jira.get_standard_tasks_info_by_sprint(sprint_id, project_name)
        standard_tasks_info_by_sprint = jira.get_filtered_task_info_by_component(standard_tasks_info_by_sprint, session["quick_filter"])
        #
        unplanned_tasks_info = jira.get_unplanned_tasks_by_sprint(sprint_id, board_id, project_name, session["quick_filter"])
        #
        raw_bug_id_list = jira.get_bug_id_by_sprint(sprint_id, board_id, project_name)
        raw_bug_id_list = jira.get_filtered_task_id_by_component(raw_bug_id_list, session["quick_filter"])
        #
        raw_bug_list = jira.get_bug_info_by_sprint(sprint_id, board_id, project_name)
        raw_bug_list = jira.get_filtered_task_info_by_component(raw_bug_list, session["quick_filter"])
        #
        change_request_id_list = jira.get_change_request_id_by_sprint(sprint_id, project_name)
        change_request_id_list = jira.get_filtered_task_id_by_component(change_request_id_list, session["quick_filter"])
        #
        raw_live_defect_id_list = jira.get_live_defect_id_by_sprint(sprint_id, project_name)
        raw_live_defect_id_list = jira.get_filtered_task_id_by_component(raw_live_defect_id_list, session["quick_filter"])
        #
        raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id, project_name)
        raw_live_defect_list = jira.get_filtered_task_info_by_component(raw_live_defect_list, session["quick_filter"])
        #
        bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id, board_id, project_name)
        bugs_opened_before_but_closed_in_sprint = jira.get_filtered_task_info_by_component(bugs_opened_before_but_closed_in_sprint, session["quick_filter"])
        #
        raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id, board_id, project_name)
        raw_automation_bug_list = jira.get_filtered_task_info_by_component(raw_automation_bug_list, session["quick_filter"])
        #
        raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id, project_name)
        raw_change_request_list = jira.get_filtered_task_info_by_component(raw_change_request_list, session["quick_filter"])
        #
        bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id, board_id, project_name, session["quick_filter"])
    else:

        standard_task_id_list = jira.get_standard_tasks_id_by_sprint(sprint_id, project_name)
        standard_tasks_info_by_sprint = jira.get_standard_tasks_info_by_sprint(sprint_id, project_name)
        #
        unplanned_tasks_info = jira.get_unplanned_tasks_by_sprint(sprint_id, board_id, project_name)
        #
        raw_bug_id_list = jira.get_bug_id_by_sprint(sprint_id, board_id, project_name)
        raw_bug_list = jira.get_bug_info_by_sprint(sprint_id, board_id, project_name)
        #
        change_request_id_list = jira.get_change_request_id_by_sprint(sprint_id, project_name)
        #
        raw_live_defect_id_list = jira.get_live_defect_id_by_sprint(sprint_id, project_name)
        #
        raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id, project_name)

        bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id, board_id, project_name)
        #
        raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id, board_id, project_name)
        #
        raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id, project_name)
        #
        bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id, board_id, project_name)

    actual_points = jira.get_actual_story_points_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

    unplanned_story_points = jira.html_get_unplanned_story_porints_by_sprint(unplanned_tasks_info)

    unplanned_nest_lists = jira.html_get_unplanned_tasks_by_sprint(unplanned_tasks_info)

    failed_nest_lists = jira.html_get_failed_tasks_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

    failed_story_points = jira.html_get_failed_story_porints_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

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
    story_share_detail = jira.html_get_bug_list_by_tasks(story_share_detail)

    render = render_template('sprint_report.html', project_required=project_name, \
                            customized_component=session["quick_filter"] if "quick_filter" in session else None, \
                            sprint_name_string=sprint_name,\
                            qa_resource = qa,\
                            sprint_status=sprint_status, actual_story_points=actual_points, \
                            unplanned_story_points=unplanned_story_points, unplanned_nest_lists=unplanned_nest_lists, \
                            failed_nest_lists=failed_nest_lists, \
                            failed_story_points = failed_story_points,\
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
                            sprint_change_request_percentage=sprint_change_request_percentage
                            )
    global response
    response = make_response(render)
    session.clear()
    return render

@app.route('/get_school_report', methods=["GET"])
def get_school_report():

    jira_account = {}
    jira_account['username'] = str(session['username'])
    jira_account['password'] = str(session['password'])

    jira = JiraHelper(config.jira_options, jira_account)

    sprint_name = session['choice_sprint']
    qa = str(session['qa_resource'])
    raw_project_name = session['project_name']

    standard_task_id_list = []
    standard_tasks_info_by_sprint = []
    unplanned_tasks_info = []
    raw_bug_id_list = []
    raw_bug_list = []
    change_request_id_list = []
    raw_live_defect_id_list = []
    raw_live_defect_list = []
    bugs_opened_before_but_closed_in_sprint = []
    raw_automation_bug_list = []
    raw_change_request_list = []
    sprint_status_list = []
    bug_trends = []

    p_name = ""
    for p in raw_project_name:
        project_name = str(p.upper())
        p_name = project_name + " " + p_name
        board_id = config.s_dict[p]
        #
        sprint_id = jira.get_sprint_id_by_sprint_name(int(board_id), sprint_name)
        #
        temp_standard_task_id_list = jira.get_standard_tasks_id_by_sprint(sprint_id, project_name)
        standard_task_id_list.append(temp_standard_task_id_list)
        #
        temp_standard_tasks_info_by_sprint = jira.get_standard_tasks_info_by_sprint(sprint_id, project_name)
        standard_tasks_info_by_sprint.append(temp_standard_tasks_info_by_sprint)
        #
        temp_unplanned_tasks_info = jira.get_unplanned_tasks_by_sprint(sprint_id, board_id, project_name)
        unplanned_tasks_info.append(temp_unplanned_tasks_info)
        #
        temp_raw_bug_id_list = jira.get_bug_id_by_sprint(sprint_id, board_id, project_name)
        raw_bug_id_list.append(temp_raw_bug_id_list)
        temp_raw_bug_list = jira.get_bug_info_by_sprint(sprint_id, board_id, project_name)
        raw_bug_list.append(temp_raw_bug_list)
        #
        temp_change_request_id_list = jira.get_change_request_id_by_sprint(sprint_id, project_name)
        change_request_id_list.append(temp_change_request_id_list)
        #
        temp_raw_live_defect_id_list = jira.get_live_defect_id_by_sprint(sprint_id, project_name)
        raw_live_defect_id_list.append(temp_raw_live_defect_id_list)
        #
        temp_raw_live_defect_list = jira.get_live_defect_info_by_sprint(sprint_id, project_name)
        raw_live_defect_list.append(temp_raw_live_defect_list)
        #
        temp_bugs_opened_before_but_closed_in_sprint = jira.get_bugs_not_found_in_sprint_but_closed_in_sprint(sprint_id, board_id, project_name)
        bugs_opened_before_but_closed_in_sprint.append(temp_bugs_opened_before_but_closed_in_sprint)
        #
        temp_raw_automation_bug_list = jira.get_automation_found_bug_info_by_sprint(sprint_id, board_id, project_name)
        raw_automation_bug_list.append(temp_raw_automation_bug_list)
        #
        temp_raw_change_request_list = jira.get_change_request_info_by_sprint(sprint_id, project_name)
        raw_change_request_list.append(temp_raw_change_request_list)
        #
        temp_sprint_status = jira.html_get_sprint_status(sprint_id, board_id)
        sprint_status_list.append(temp_sprint_status)
        #
        temp_bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id, board_id, project_name)
        bug_trends.append(temp_bug_trends)

    # Remove the duplicated value and format the list to next use.
    standard_task_id_list = jira.remove_nested_list_duplicated_value(standard_task_id_list)
    standard_tasks_info_by_sprint = jira.remove_nested_list_duplicated_value(standard_tasks_info_by_sprint)
    unplanned_tasks_info = jira.remove_nested_list_duplicated_value(unplanned_tasks_info)
    raw_bug_id_list = jira.remove_nested_list_duplicated_value(raw_bug_id_list)
    raw_bug_list = jira.remove_nested_list_duplicated_value(raw_bug_list)
    change_request_id_list = jira.remove_nested_list_duplicated_value(change_request_id_list)
    raw_live_defect_id_list = jira.remove_nested_list_duplicated_value(raw_live_defect_id_list)
    raw_live_defect_list = jira.remove_nested_list_duplicated_value(raw_live_defect_list)
    bugs_opened_before_but_closed_in_sprint = jira.remove_nested_list_duplicated_value(bugs_opened_before_but_closed_in_sprint)
    raw_automation_bug_list = jira.remove_nested_list_duplicated_value(raw_automation_bug_list)
    raw_change_request_list = jira.remove_nested_list_duplicated_value(raw_change_request_list)
    bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint_and_project(bug_trends)

    # generate report
    actual_points = jira.get_actual_story_points_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

    unplanned_story_points = jira.html_get_unplanned_story_porints_by_sprint(unplanned_tasks_info)

    unplanned_nest_lists = jira.html_get_unplanned_tasks_by_sprint(unplanned_tasks_info)

    failed_nest_lists = jira.html_get_failed_tasks_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

    failed_story_points = jira.html_get_failed_story_porints_by_sprint(sprint_id, board_id, standard_tasks_info_by_sprint)

    sprint_bug_nested_list = jira.html_get_bug_list_by_tasks(raw_bug_list)

    previous_bugs_closed_in_sprint = jira.html_get_bug_list_by_tasks(bugs_opened_before_but_closed_in_sprint)

    sprint_automation_bug_list = jira.html_get_bug_list_by_tasks(raw_automation_bug_list)
    sprint_automation_bug_percentage = jira.html_get_automation_found_bug_percentange(raw_bug_id_list, raw_automation_bug_list)

    sprint_live_defect_nested_list = jira.html_get_bug_list_by_tasks(raw_live_defect_list)
    sprint_live_defect_percentage = jira.html_get_live_defect_percentage_of_all_defects(raw_live_defect_id_list, raw_bug_id_list )

    sprint_change_request_nested_list = jira.html_get_bug_list_by_tasks(raw_change_request_list)
    sprint_change_request_percentage = jira.html_get_change_request_percentage_of_all_defects(standard_task_id_list, change_request_id_list)

    bug_priority_list = jira.html_get_share_ratio_by_priority(raw_bug_list)
    bug_priority_detail = jira.html_get_share_ratio_detail_by_priority(raw_bug_list)

    story_list= jira.get_task_id_that_has_linked_task(raw_bug_id_list)
    story_share = jira.html_get_linked_issue_num_group_by_story(story_list)
    story_share_detail = jira.html_get_linked_issue_detail_group_by_story(story_list, raw_bug_id_list)[1]
    story_share_detail = jira.html_get_bug_list_by_tasks(story_share_detail)
    sprint_status = jira.html_get_mulitple_sprint_status(sprint_status_list)

    render = render_template('sprint_report.html', project_required=p_name.strip(), \
                            customized_component=session["quick_filter"] if "quick_filter" in session else None, \
                            sprint_name_string=sprint_name,\
                            qa_resource = qa,\
                            sprint_status=sprint_status, actual_story_points=actual_points, \
                            unplanned_story_points=unplanned_story_points, unplanned_nest_lists=unplanned_nest_lists, \
                            failed_nest_lists=failed_nest_lists, \
                            failed_story_points = failed_story_points,\
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
                            sprint_change_request_percentage=sprint_change_request_percentage
                            )
    global response
    response = make_response(render)
    session.clear()
    return render

if __name__ == '__main__':
    # app.run(debug=True, threaded=False)
    app.run(host="0.0.0.0", debug=False, threaded=True)