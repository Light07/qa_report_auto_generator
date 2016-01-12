# -*- coding: utf-8 -*-
__author__ = 'kevin.cai'

import settings
from pages.jira_helper import JiraHelper
from pages.html_report_helper import HTML_Report

if __name__ == '__main__':
    jira = JiraHelper(settings.jira_options, settings.jira_account)
    h = HTML_Report()

    sprint_name = "Sprint 1517 (12/28 - 01/15)"
    sprint_id = jira.get_sprint_id_by_sprint_name(settings.board_id, sprint_name)

    sprint_status = jira.html_get_sprint_status(sprint_id)

    actual_points = jira.html_get_actual_story_points_by_sprint(sprint_id)

    #
    raw_bug_list =jira.get_bug_info_by_sprint(sprint_id)
    sprint_bug_nested_list = jira.html_get_bug_list_by_tasks(raw_bug_list)

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

    # #
    story_list= jira.get_task_id_that_has_linked_task(sprint_id)
    story_share = jira.html_get_linked_issue_num_group_by_story(story_list)
    story_share_detail = jira.html_get_linked_issue_detail_group_by_story(sprint_id, story_list)

    #
    bug_trends = jira.html_get_total_bug_and_open_bug_trend_by_sprint(sprint_id)

    h.generate_report(sprint_name, sprint_status, actual_points, sprint_bug_nested_list,\
                      bug_priority_list, bug_priority_detail,\
                      story_share, story_share_detail,\
                      bug_trends,\
                      sprint_automation_bug_list, sprint_automation_bug_percentage,\
                      sprint_live_defect_nested_list, sprint_live_defect_percentage,\
                      sprint_change_request_nested_list, sprint_change_request_percentage)
