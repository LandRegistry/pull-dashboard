"""
Data objects
"""
from datetime import datetime
class PullRequest(object):
    def __init__(self, number, title, user, created_at, repo_name, pull_url):
        self.number = number
        self.title = title
        self.user = user
        self.created_at = created_at
        self.repo_name = repo_name
        self.pull_url = pull_url

		# Determine how old the record is
        now = datetime.now()
        then = datetime.fromtimestamp(self.created_at)
        tdelta = now - then
        self.days_old = tdelta.days
        self.hours_old = tdelta.seconds // 3600


class JenkinsProject(object):
    def __init__(self, name, url, status, timestamp, culprits, buildid):
        self.name = name
        self.url = url
        self.status = status
        self.timestamp = timestamp
        self.culprits = culprits
        self.buildid = buildid
