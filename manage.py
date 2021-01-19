from flask_script import Manager
from flask_migrate import MigrateCommand
from appvars import app
from velocity import make_velocity_report

app.config.from_object("config.Config")

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def update_velocity_data():
    """
    Update velocity data
    """
    return make_velocity_report()


if __name__ == '__main__':
    manager.run()
