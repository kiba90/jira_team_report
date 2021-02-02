from jira import JIRA
from datasources import resources
from models import Velocity
from models import Projects
from models import Worklog
from config import LOGGER_FORMAT
from datasources import boards
import logging
from appvars import db

logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)


def make_velocity_report():
    v = resources.VelocityInfo(JIRA)
    for board in boards.BOARD_LIST.values():
        data = v.velocity_stat_entries(board)
        for item in data:

            if item['project_key'] in item['name'][:len(item['project_key'])]:
                Velocity.create_new_report(item)

            else:
                logging.info('Wrong sprint item in project ' + item['project_key'] +
                             ' sprint_id: ' + str(item['sprint_id']) +
                             ' sprint_name: ' + item['name'])
                pass
    return


def worklog_stats():
    """
    Getting worklog stats of completed issues in sprint
    :return: total worklog of completed issues
    """
    fl = resources.FlowEfficiency(JIRA)
    for project, board in boards.BOARD_LIST.items():
        sprint_list = db.session.query(Velocity).join(Projects).filter(Projects.project_key == project).all()
        for sprint in sprint_list:
            worklog = fl.completed_issue(board, sprint.sprint_id)
            logged_time_stat = {
                'project_id': sprint.project_id,
                'sprint_id': sprint.sprint_id,
                'worklog': worklog
            }
            Worklog.create_new_worklog(logged_time_stat)