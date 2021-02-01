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
    sprint_id = Column(db.INTEGER, nullable=False, unique=True, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jira_projects.id'), nullable=False)
    name = Column(db.VARCHAR(length=256), nullable=False)
    commitment = Column(db.FLOAT(), nullable=False)
    completed = Column(db.FLOAT(), nullable=False)
    start_at = Column(db.TIMESTAMP(), nullable=False)
    end_at = Column(db.TIMESTAMP(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_key = db.relationship('Projects', backref=db.backref('project_name', lazy='dynamic'))

    @staticmethod
    def create_new_report(data):
        """
        :param data: dict
        :return:
        """
        data['project_key'] = Projects.query.filter_by(project_key=data['project_key']).first()
        exists = db.session.query(Velocity.sprint_id).filter_by(sprint_id=data['sprint_id']).scalar() is not None
        if not exists:
            report = Velocity(**data)
            db.session.add(report)
            logging.info('Create a new velocity data ' + str(report.project_key.project_key) + ' ' + str(report.name))
            db.session.commit()
        else:
            logging.info('Nothing changed, sprint_id: ' + str(data['sprint_id']) + ' already exist')


class FlowEfficiency(db.Model):

    __tablename__ = 'jira_work_stat'
    id = Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jira_projects.id'), nullable=False)
    sprint_id = db.Column(db.Integer, db.ForeignKey('jira_velocity.sprint_id'), nullable=False)
    worklog = Column(db.INTEGER, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Projects(db.Model):
    __tablename__ = 'jira_projects'
    id = Column(db.Integer, primary_key=True)
    project_key = Column(db.VARCHAR(length=256), nullable=False, unique=True)

