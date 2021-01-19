from munch import munchify
from jira import JIRA
import datetime
from config import JiraConfig
from datasources import boards

DATE_FORMAT = '%d/%b/%y %H:%M %p'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def string2datetime(value):
    """ Covert string to datetime"""
    conv_date = datetime.datetime.strptime(value, DATE_FORMAT)
    return conv_date.strftime(DATETIME_FORMAT)


def get_project_by_board_id(board_list, board_id):
    board_list = board_list
    board_id = board_id
    for key, value in board_list.items():
        if value == board_id:
            return key


class VelocityInfo(JIRA):

    def __init__(self, options=None, basic_auth=None):
        JIRA.__init__(self, options=JiraConfig.JIRA_OPTIONS, basic_auth=(JiraConfig.LOGIN, JiraConfig.PASS))

    def get_velocity_report(self, board_id):
        """
        Getting velocity by GreenHopper API
        :return: json with last 7 sprints
        """
        r = self._get_json('rapid/charts/velocity?rapidViewId=%s' % board_id, base=JIRA.AGILE_BASE_URL)
        r['project_key'] = get_project_by_board_id(boards.BOARD_LIST, board_id)
        return r

    def sprint_duration_info(self, sprint_id):
        """
        :param sprint_id: id of sprint
        :return: list of start / end dates
        """
        result = self.sprint(id=sprint_id)
        sprint_durations = {
            'sprint_id': result.raw['id'],
            'name': result.raw['name'],
            'start_at': result.raw['startDate'],
            'end_at': result.raw['endDate']
        }
        return sprint_durations

    def velocity_stat_entries(self, board_id):
        """
        velocityStatEntries  data of velocity (commitment / completed ) by sprint
        sprints - id and sprint's name
        :param board_id:
        :return: array of sprint sprint_id, project key, sprint name, velocity and duration
        """

        data = munchify(self.get_velocity_report(board_id))
        result_list = []
        for sprint in data.sprints:
            sprint_id = int(sprint['id'])
            sprints = {
                'project_key': data['project_key'],
                'sprint_id': sprint['id'],
                'name': sprint['name'],
            }
            for velocity in data.velocityStatEntries:
                if int(velocity) == sprint['id']:
                    sprints['commitment'] = data.velocityStatEntries[velocity]['estimated']['value']
                    sprints['completed'] = data.velocityStatEntries[velocity]['completed']['value']

            if sprints['name'][:3] in sprints['project_key']:
                duration = self.sprint_duration_info(sprint_id)
                sprints['start_at'] = string2datetime(duration['start_at'])
                sprints['end_at'] = string2datetime(duration['end_at'])

            elif sprints['name'][:2] in sprints['project_key']:
                duration = self.sprint_duration_info(sprint_id)
                sprints['start_at'] = string2datetime(duration['start_at'])
                sprints['end_at'] = string2datetime(duration['end_at'])

            result_list.append(sprints)
        return result_list
