# -*- coding: utf-8 -*-
import os
import settings
class HTML_Report(object):

    report_template_file = None
    report_folder = None
    report_file = None

    def __init__(self):
        _root_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.report_folder = os.path.join(_root_folder, 'report')
        if not os.path.exists(self.report_folder):
            os.mkdir(self.report_folder)

        self.report_template_file = os.path.join(self.report_folder, 'report_template.html')

    def read_file(self, file_path=report_template_file, mode="r"):
        with open(self.report_template_file, mode = mode) as f:
            return "".join(f.readlines())

    def format_sprint_name(self, sprint_name):
        sprint_name = str(sprint_name).replace(" ", "_")
        sprint_name = sprint_name.replace("(", "")
        sprint_name = sprint_name.replace(")", "")
        sprint_name = sprint_name.replace("/", "-")
        return sprint_name

    def generate_report\
                    (self, sprint_name, sprint_status, actual_points, all_bug_list,\
                     bug_priority_share_list, bug_priority_share_detail,\
                     story_share_list, story_share_detail,\
                     total_bug_and_opened_bug_pair_list,\
                     automation_found_bug_list, automation_percentage,\
                     live_defect_list, live_defect_percentage,\
                     change_request_list, change_request_percentage
                     ):
        '''
        :param sprint_name:
        :param all_bug_list: eg:
            [
                ['bug_id-1', 'priority', 'summary', 'status'],
                ['bug_id-1', 'priority', 'summary', 'status']
            ]
        :param bug_priority_share_list: eg:
            [
                ['priority', 'number'],
                ['Blocker', 1],
                ['Major', 5],
                ['Critical', 1],
                ['Minor', 2]
            ]
        :param bug_priority_share_detail:eg:
            [
                ['Blocker', ['ATEAM-3913']],
                ['Major', ['ATEAM-3922', 'ATEAM-3941'] ],
                ['Critical', ['ATEAM-3919']],
                ['Minor', ['ATEAM-3921', 'ATEAM-3920']]
            ]
        :param total_bug_and_opened_bug_pair_list:eg:
            [
                ['Date',  'total bug number', 'Opened bug number'],
                ['2015-12-07', 0, 0], ['2015-12-08', 0, 0], ['2015-12-09', 0, 1], ['2015-12-10', 2, 3], ['2015-12-11', 3, 5], ['2015-12-12', 4, 6]
             ]
        :return:  N/A
        '''
        formatted_sprint_name = self.format_sprint_name(sprint_name)
        self.report_file = os.path.join(self.report_folder, '{sprint}.html'.format(sprint=formatted_sprint_name))
        contents = self.read_file()
        contents = contents.replace("{sprint_name_string}", str(sprint_name))
        contents = contents.replace("{qa_resource}", str(settings.qa_resource))



        contents = contents.replace("{sprint_status}", str(sprint_status))
        contents = contents.replace("{actual_story_points}", str(actual_points))


        contents = contents.replace("{sprint_bug_nested_lists}", str(all_bug_list))

        contents = contents.replace("{bug_priority_nested_lists}", str(bug_priority_share_list))
        contents = contents.replace("{bug_priority_share_detail_info}", str(bug_priority_share_detail))

        contents = contents.replace("{story_share_nested_lists}", str(story_share_list))
        contents = contents.replace("{story_share_detail_info}", str(story_share_detail[1]))

        contents = contents.replace("{total_bug_and_opened_bug_pair_nested_list}", str(total_bug_and_opened_bug_pair_list))


        contents = contents.replace("{sprint_live_defect_nested_lists}", str(live_defect_list))
        contents = contents.replace("{sprint_live_defect_percentage}", str(live_defect_percentage))

        contents = contents.replace("{sprint_automation_found_bug_nested_lists}", str(automation_found_bug_list))
        contents = contents.replace("{sprint_automation_bug_percentage}", str(automation_percentage))

        contents = contents.replace("{sprint_change_request_nested_lists}", str(change_request_list))
        contents = contents.replace("{sprint_change_request_percentage}", str(change_request_percentage))

        with open(self.report_file, "w") as f:
            f.writelines(contents)