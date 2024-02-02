"""
Creates a utility to close pull requests opened by Dependabot. These are pull requests
that we just do not want to deal with.

1. Get open pull requests.
2. Filter pull requests opened by Dependabot.
3. Create a comment telling Dependabot to ignore that dependency.
4. Close the pull request.

See https://docs.github.com/en/code-security/dependabot
See https://docs.github.com/en/rest/pulls/pulls
"""

import json
import os
import requests


api_origin = 'https://api.github.com'
accept_header = 'application/vnd.github+json'
api_version_header = '2022-11-28'
dependabot_user_login = 'dependabot[bot]'


def get_open_pull_requests(repo_owner: str, repo_name: str, github_token: str, **kwargs):
    """
    Get open pull requests.

    If the request succeeds, return the JSON response body. If the request fails,
    raise an exception.

    See https://docs.github.com/en/rest/pulls/pulls?apiVersion=2022-11-28#list-pull-requests
    """
    per_page = int(kwargs.get('per_page', '100'))
    state = kwargs.get('state', 'open')

    url = f'{api_origin}/repos/{repo_owner}/{repo_name}/pulls?per_page={per_page}&state={state}'
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': accept_header,
        'X-GitHub-Api-Version': api_version_header,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to get open pull requests for {repo_owner}/{repo_name}. Status code: {response.status_code}, response: {response.text}')


def create_pull_request_comment(repo_owner: str, repo_name: str, pull_number: int, github_token: str):
    """
    Create a new pull request comment. This comment will tell Dependabot to ignore
    this library in the future.

    Per the GitHub API documentation, pull requests are a type of issue. "Every pull request is an issue, but not
    every issue is a pull request." PR-level comments are handled by the issue API.

    See https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#create-an-issue-comment
    """
    url = f'{api_origin}/repos/{repo_owner}/{repo_name}/issues/{pull_number}/comments'
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Accept': accept_header,
        'X-GitHub-Api-Version': api_version_header,
    }
    data = {
        'body': '@dependabot ignore this dependency'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print(f"Added comment to PR #{pull_number} for {repo_owner}/{repo_name}")
        return response.json()
    else:
        raise Exception(f"Failed to add comment to PR #{pull_number} for {repo_owner}/{repo_name}. Status code: {response.status_code}, response: {response.text}")


try:
    repo_owner = 'EliLillyCo'
    # repo_name = 'aads_vahub_web_projects'
    repo_name = 'aads_vahub_homepage'
    github_token = os.environ.get('GITHUB_TOKEN')

    if github_token is None:
        raise Exception('Could not find GITHUB_TOKEN environment variable')

    pull_requests = get_open_pull_requests(repo_owner, repo_name, github_token, state='open', per_page=30)

    # If there are no pull requests, then exit. There is nothing to do.
    if len(pull_requests) == 0:
        print(f'There are no open pull requests for {repo_owner}/{repo_name}')
        exit(0)

    print(f"Pull requests for {repo_owner}/{repo_name}:")

    for pull_request in pull_requests:
        # We can only close open PRs. If the state is anything else, go on to the
        # next PR.
        if pull_request['state'] != 'open':
            print(f"PR #{pull_request['number']} is {pull_request['state']} (skip)")
            continue

        # We are only going to close PRs that were opened by Dependabot.
        if pull_request['user']['login'] == dependabot_user_login:
            print(f"PR #{pull_request['number']} was opened by {pull_request['user']['login']}")
        else:
            print(f"PR #{pull_request['number']} is not opened by a bot (skip)")
            continue

        create_pull_request_comment(repo_owner, repo_name, pull_request['number'], github_token)

except Exception as e:
    print(f"Error: {e}")
    exit(1)

