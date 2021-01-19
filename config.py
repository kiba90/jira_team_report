import os

LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['POSTGRESQL_URI']


class JiraConfig:
    LOGIN = os.environ['JIRA_LOGIN']
    PASS = os.environ['JIRA_PASS']
    JIRA_OPTIONS = {'server': os.environ['JIRA_BASE_URL']}