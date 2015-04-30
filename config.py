import os


class Config(object):
    DEBUG = False
    REPOSITORY_BLACKLIST = 'Blacklistfile'
    GITHUB_API_ISSUES_URL = "https://api.github.com/orgs/LandRegistry/issues"
    # split parameter out so URL config var can be used for response mocking
    GITHUB_API_ISSUES_FILTER = "?filter=all"
    GITHUB_API_HEADERS = {
        'User-Agent': 'LandRegistry-Build-Dashboard/1.0.0',
        'Accept': 'application/vnd.github.v3+json',
        'Content-type': 'application/json',
        'Authorization': 'token %s' % os.environ.get('GITHUB_API_KEY')
    }
    JENKINS_URL = os.environ.get(
        'JENKINS_HOST') + '/api/json?pretty=true&depth=2&&tree=jobs[name,buildable,lastBuild[number,duration,timestamp,culprits[fullName],result,url,changeSet[items[msg,author[fullName]]]]]'
    JENKINS_USER = os.environ.get('JENKINS_USER')
    JENKINS_PASSWORD = os.environ.get('JENKINS_PASSWORD')


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True
