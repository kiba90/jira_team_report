from munch import munchify
from jira import JIRA
import datetime
from config import JiraConfig
from datasources import boards
from dateutil.parser import parse

DATE_FORMAT = '%d/%b/%y %H:%M %p'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def string2datetime(value):
    """ Covert string to datetime"""
    conv_date = datetime.datetime.strptime(value, DATE_FORMAT)
    return conv_date.strftime(DATETIME_FORMAT)


def get_project_by_board_id(board_list, board_id):
    for key, value in board_list.items():
        if value == board_id:
            return key


class VelocityInfo(JIRA):
    """
    The Velocity report shows the amount of value delivered in each sprint, enabling you to predict the amount of work the team can get done in future sprints.
    It is useful during your sprint planning meetings, to help you decide how much work you can feasibly commit to.

    -- Commitment: for each sprint shows the total estimate of all issues in the sprint when it begins.
    After the sprint has started, any stories added to the sprint, or any changes made to estimates, will not be included in this total.
    -- Completed: The green bar in each sprint shows the total completed estimates when the sprint ends.
    Any scope changes made after the sprint started are included in this total.
    -- Velocity report gets for the last 7 sprints completed by the team.

    method get_velocity_report - Getting full report of scrum board for last 7 sprints
    method sprint_duration_info - Provides dates of start / completed days
    method velocity_stat_entries - Preparing the list of a sprints for scrum board
    """

    def __init__(self, options=None, basic_auth=None):
        JIRA.__init__(self, options=JiraConfig.JIRA_OPTIONS, basic_auth=(JiraConfig.LOGIN, JiraConfig.PASS))

    def get_velocity_report(self, board_id):
        """
        Getting velocity by Jira GreenHopper API
        :return: last 7 sprints for a scrum board
        """
        r = self._get_json('rapid/charts/velocity?rapidViewId=%s' % board_id, base=JIRA.AGILE_BASE_URL)
        r['project_key'] = get_project_by_board_id(boards.BOARD_LIST, board_id)
        return r

    def sprint_duration_info(self, sprint_id: int):
        """
        :param sprint_id: id of sprint
        :return: Dict of start / completed dates
        """
        result = self.sprint(id=sprint_id)
        sprint_durations = {
            'sprint_id': result.raw['id'],
            'name': result.raw['name'],
            'start_at': result.raw['startDate'],
            'end_at': result.raw['completeDate']
        }
        return sprint_durations

    def velocity_stat_entries(self, board_id):
        """
        velocityStatEntries the data of velocity (commitment / completed in seconds ) by sprint
        sprints - id and sprint's name
        :param board_id:
        :return: array of sprints -> sprint_id, project key, name, velocity and duration
        """
        # Make object from Json
        data = munchify(self.get_velocity_report(board_id))

        result_list = []
        for sprint in data.sprints:
            sprints = {
                'project_key': data['project_key'],
                'sprint_id': sprint['id'],
                'name': sprint['name'],
            }
            for velocity in data.velocityStatEntries:
                if int(velocity) == sprint['id']:

                    # Sum of original time estimation in commitment / completed in seconds
                    sprints['commitment'] = data.velocityStatEntries[velocity]['estimated']['value']
                    sprints['completed'] = data.velocityStatEntries[velocity]['completed']['value']

            # Checking sprint name, the spirit's name should be started with Jira project key!
            if sprints['name'][:len(sprints['project_key'])] in sprints['project_key']:
                duration = self.sprint_duration_info(int(sprint['id']))
                sprints['start_at'] = string2datetime(duration['start_at'])
                sprints['end_at'] = string2datetime(duration['end_at'])

            result_list.append(sprints)
        return result_list


class FlowEfficiency(JIRA):
    """
    Getting sprint report with completed / not completed issues and calculating worklog
    -- method get_sprint_report() - getting full jira sprint report
    -- method calculate_worklog() - calculating worklog time in seconds for all task in sprint
    -- method dev_count() - calculating number of developers in the sprint
     """

    def __init__(self, options=None, basic_auth=None):
        JIRA.__init__(self, options=JiraConfig.JIRA_OPTIONS, basic_auth=(JiraConfig.LOGIN, JiraConfig.PASS))

    def get_sprint_report(self, board_id, sprint_id):
        """
        Getting full sprint report
        :param board_id: id of scrum board in jira
        :param sprint_id: id of sprint in jira
        :return:
        """
        return self._get_json('rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (board_id, sprint_id),
                              base=JIRA.AGILE_BASE_URL)

    def dev_count(self, project_key, sprint_id):
        """
        Count of unique developers(assignee) in the sprint.
        :param project_key: str
        :param sprint_id: int
        :return: count: int
        """
        issue_list = self.search_issues(jql_str='project = ' + project_key + ' and sprint = ' + str(sprint_id))
        dev = []
        for issue in issue_list:
            try:
                dev.append(issue.fields.assignee.key)
            except AttributeError:
                pass
        return len(set(dev))

    def calculate_worklog(self, report, sprint_info):
        """
        Calculating worklog time of completed issues during a sprint
        :param report:
        :param sprint_info:
        :return: Total logged time in seconds. type: int
        """
        total_time = 0
        for issue in report:
            worklogs = self.worklogs(issue['key'])
            for worklog in worklogs:

                # time when worklog commited was
                w_time = parse(worklog.created)

                # sprint start / end dates
                s_start_time = parse(sprint_info['startDate'])
                s_end_time = parse(sprint_info['completeDate'])

                if s_start_time.date() <= w_time.date() <= s_end_time.date():
                    total_time += worklog.timeSpentSeconds
        return total_time
