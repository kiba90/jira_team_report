from jira import JIRA
from datasources import resources
from models import Velocity
from config import LOGGER_FORMAT
from datasources import boards
import logging

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

