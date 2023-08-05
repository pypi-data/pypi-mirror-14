import datetime
import re
import requests
from invisibleroads_macros.disk import cd
from invisibleroads_macros.shell import run_command
from os import getcwd
from pytz import timezone
from tzlocal import get_localzone

from .exceptions import BadCommitHash, BadRepository, BadRepositoryURL, BadURL


__all__ = [
    'download_github_repository',
    'update_github_repository',
    'get_github_repository_url',
    'get_github_repository_folder',
    'get_github_repository_commit_hash',
    'get_github_repository_commit_timestamp',
    'get_github_ssh_url',
    'get_github_https_url',
    'parse_github_url',
    'run_git',
    'validate_github_commit_hash',
    'get_github_user_properties',
    'get_github_user_nickname',
]
GITHUB_URL_PATTERN = re.compile(
    r'github.com[/:]([a-zA-Z0-9-]+)/([a-zA-Z0-9-_]+)(?:\.git)?$')


def download_github_repository(target_folder, github_url):
    github_url = get_github_ssh_url(github_url)
    run_git(['git', 'clone', github_url, target_folder])
    return get_github_repository_commit_hash(target_folder)


def update_github_repository(folder):
    run_git('git fetch', folder)
    return get_github_repository_commit_hash(folder)


def get_github_repository_url(folder=None):
    github_url = run_git('git config --get remote.origin.url', folder)
    return get_github_https_url(github_url)


def get_github_repository_folder(folder=None):
    return run_git('git rev-parse --show-toplevel', folder)


def get_github_repository_commit_hash(folder=None):
    return run_git('git rev-parse HEAD', folder)


def get_github_repository_commit_timestamp(
        folder=None, commit_hash=None, to_utc=False):
    update_github_repository(folder)
    timestamp_string = run_git([
        'git', 'show', '-s', '--date=local', '--format=%cd', commit_hash or '',
    ], folder)
    local_timestamp = datetime.datetime.strptime(
        timestamp_string, '%a %b %d %H:%M:%S %Y')
    local_timezone = get_localzone()
    timestamp = local_timezone.localize(local_timestamp)
    if to_utc:
        timestamp = timestamp.astimezone(timezone('UTC'))
    return timestamp


def get_github_ssh_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'git@github.com:%s/%s.git' % (user_name, repository_name)


def get_github_https_url(github_url):
    user_name, repository_name = parse_github_url(github_url)
    return 'https://github.com/%s/%s' % (user_name, repository_name)


def parse_github_url(github_url):
    try:
        return GITHUB_URL_PATTERN.search(github_url).groups()
    except AttributeError:
        m = 'Could not parse as GitHub URL (github_url = %s)'
        raise BadRepositoryURL(m % github_url)


def run_git(command_args, folder=None, exception_by_error=None):
    if not folder:
        folder = getcwd()
    exception_by_error = dict({
        'Could not read': BadURL,
        'Not a git repository': BadRepository,
        'not found': BadURL,
        'not a tree object': BadCommitHash,
        'Not a valid object name': BadCommitHash,
    }, **(exception_by_error or {}))
    with cd(folder):
        output = run_command(command_args, exception_by_error)
    return str(output)  # Convert bytes to str in Python 3


def validate_github_commit_hash(commit_hash):
    commit_hash = commit_hash.strip()
    match = re.search(r'[^a-zA-Z0-9]+', commit_hash)
    if match:
        raise BadCommitHash
    return commit_hash


def get_github_user_properties(username):
    response = requests.get('https://api.github.com/users/%s' % username)
    response_json = response.json()
    if 'message' in response_json:
        return
    return response_json


def get_github_user_nickname(username):
    user_properties = get_github_user_properties(username)
    if not user_properties:
        return
    return user_properties['name']
