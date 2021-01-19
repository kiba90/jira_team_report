import logging
from config import LOGGER_FORMAT
from appvars import db
from sqlalchemy import Column
from datetime import datetime

logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)


class Velocity(db.Model):
    """
    Jira velocity statistic
    """
    __tablename__ = 'jira_velocity'

    id = Column(db.Integer, primary_key=True)
    project_key = Column(db.VARCHAR(length=256), nullable=False)
    sprint_id = Column(db.INTEGER, nullable=False, unique=True)
    name = Column(db.VARCHAR(length=256), nullable=False, unique=True)
    commitment = Column(db.FLOAT(), nullable=False)
    completed = Column(db.FLOAT(), nullable=False)
    start_at = Column(db.TIMESTAMP(), nullable=False)
    end_at = Column(db.TIMESTAMP(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def create_new_report(data):
        """
        :param data: dict
        :return:
        """
        report = Velocity(**data)
        exists = db.session.query(Velocity.sprint_id).filter_by(sprint_id=report.sprint_id).scalar() is not None
        if not exists:
            db.session.add(report)
            logging.info('Create a new velocity data')
            db.session.commit()
        else:
            logging.info('Nothing changed, sprint_id: ' + str(report.sprint_id) + ' already exist')


