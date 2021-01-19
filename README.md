# Jira team's report

Service for old jira server v7 to collect velocity data in PostgreSQL

# Requirements

- Python
- SQLAlchemy supported database (PostgreSQL)

# Installation

Install requirements:

```
pip install -r requiremets
```

Set database URI environment variable:
```python
export POSTGRESQL_URI=<your database uri>
```

Set jira environment variable:
```python
export JIRA_BASE_URL=<your url ex. https://my-jira.com>
export JIRA_LOGIN=<your login>
export JIRA_PASS=<your password>
```

Set up database:
```
python manage.py db upgrade
```

Do not forget to create your own scrum board list in /datasources/boards.py in format:
```python
'project key in jira': <scrum board id>
```

Because all search based on scrum board id


# Usage

The following command updates the data in the project database.
```
python manage.py update_velocity_data
```
