from flask_script import Manager
from flask_migrate import MigrateCommand
from appvars import app
from reports import make_velocity_report
from reports import worklog_stats

app.config.from_object("config.Config")

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def update_velocity_data():
    """
    Update velocity data
    """
    return make_velocity_report()

@manager.command
def update_worklog_data():
    """
    Update worklog statistics for completed issue by sprint
    :return:
    """
    return worklog_stats()


if __name__ == '__main__':
    manager.run()
