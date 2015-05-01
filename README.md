# pull-dashboard

For this to run, you will need a Github access key in your environment, called GITHUB_API_KEY. All it needs is Land registry public repos read access.

## Running

```bash
sudo pip install -r requirements.txt
export GITHUB_API_KEY=<key>
export JENKINS_HOST=<host> (with protocol and without trailing slash, e.g. http://127.0.0.1)
export JENKINS_USER=<user>
export JENKINS_PASSWORD=<password>
./run_flask_dev.py
```

## Configuration

The list of repositories to exclude are in held in the file pointed to by the config.py::REPOSITORY_BLACKLIST entry. Currently this is 'Blacklistfile'.
