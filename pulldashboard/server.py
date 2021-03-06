from flask import render_template
from pulldashboard import app
from pulldashboard.models import PullRequest, JenkinsProject
from pulldashboard import excludedRepos
import requests
import time
import re
from calendar import timegm


@app.route('/')
def index():
    """
    Constructs the index page.
    """
    url = app.config['GITHUB_API_ISSUES_URL'] + \
        app.config['GITHUB_API_ISSUES_FILTER']

    pulls = []
    ciprojects = []

    # Required headers for a GET request
    response = requests.get(url, headers=app.config['GITHUB_API_HEADERS'])
    if response.status_code == requests.codes.ok:
        raw_issues = response.json()
        for raw_issue in raw_issues:
            # Check blacklist
            if raw_issue['repository']['full_name'] in excludedRepos:
                break

            # Check if issue is actually a pull request and add to list if it
            # is
            if 'pull_request' in raw_issue:
                pull_request = PullRequest(
                    raw_issue['number'],
                    raw_issue['title'],
                    raw_issue['user']['login'],
                    timegm(time.strptime(
                        raw_issue['created_at'].replace('Z', 'GMT'), '%Y-%m-%dT%H:%M:%S%Z')),
                    raw_issue['repository']['name'],
                    raw_issue['html_url']
                )
                pulls.append(pull_request)
    try:
        response = requests.get(app.config['JENKINS_URL'], auth=(
            app.config['JENKINS_USER'], app.config['JENKINS_PASSWORD']))
        if response.status_code == requests.codes.ok:
            jenkins_raw = response.json()
            for jenkins_projects in jenkins_raw['jobs']:

                result = re.findall(
                    r'\(Controller\)', jenkins_projects['name'])
                if len(result) == 0:
                    result = re.findall(
                        r'\(Branch\)', jenkins_projects['name'])
                    if len(result) == 0:

                        if jenkins_projects['buildable'] == True:
                            try:
                                status = 'Failing'
                                if jenkins_projects['lastBuild']['building'] == True:
                                    status = 'Inprogress'
                                if jenkins_projects['lastBuild']['result'] == 'SUCCESS':
                                    status = 'Passing'

                                url = jenkins_projects['lastBuild']['url']
                                timestamp = jenkins_projects[
                                    'lastBuild']['timestamp']
                                culprits = jenkins_projects[
                                    'lastBuild']['culprits']
                                number = jenkins_projects[
                                    'lastBuild']['number']

                            except Exception:
                                status = 'Notrun'
                                url = ''
                                timestamp = ''
                                culprits = ''
                                number = '0'

                            ciproject = JenkinsProject(
                                jenkins_projects['name'],
                                url,
                                status,
                                timestamp,
                                culprits,
                                number
                            )
                            ciprojects.append(ciproject)

        # Sort by time, oldest first as that's the most important to sort out
        pulls.sort(key=lambda x: x.created_at, reverse=False)
        ciprojects.sort(key=lambda x: x.status, reverse=False)

        return render_template("index.html", pulls=pulls, ciprojects=ciprojects)

    except Exception as exc:
        return render_template(
            "jenkins_error.html", jenkins_url=app.config['JENKINS_URL'], error=exc)


@app.after_request
def after_request(response):
    """
    Some useful headers to set to beef up the robustness of the app
    https://www.owasp.org/index.php/List_of_useful_HTTP_headers
    """
    response.headers.add('Content-Security-Policy',
                         ("default-src 'self' ajax.googleapis.com maxcdn.bootstrapcdn.com "
                          "fonts.gstatic.com fonts.googleapis.com data:"))
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
