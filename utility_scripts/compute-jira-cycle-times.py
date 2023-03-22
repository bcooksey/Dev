#-*- coding: utf-8 -*-
import csv
import json
import sys
import requests
from datetime import datetime, timedelta

credentials = {}
if len(sys.argv) < 3:
    print('Usage: get-jira-cycle-time <path_to_credentials> <path_to_jira_export>')
    exit()

with open(sys.argv[1], 'r') as _file:
    credentials = json.loads(_file.read())

BASE_URL = 'https://{}.atlassian.net/rest/api/2/'.format(credentials['subdomain'])
CACHE_DIR = 'jira-data'
csv_headers = [
    # These should match the headings exported out of Jira
    'Issue Type',
    'Issue key',
    'Issue id',
    'Summary',
    'Assignee',
    'Reporter',
    'Status',
    'Resolution',
    'Created',
    'Story Points',
    'Resolved',
    # These are going to be added by this script
    'First In Progress',
    'Last In Progress',
    'Done',
    'Cycle Time (F)',
    'Cycle Time (L)',
]

session = requests.Session()
session.headers.update({'Authorization': 'Bearer {}'.format(credentials['token'])})

def get_issue_list_from_csv():
    issues = []
    with open(sys.argv[2], 'r') as _file:
        csv_file = csv.DictReader(_file)
        for row in csv_file:
            issues.append(row)
    return issues

def get_issue_list_from_hard_coded():
    return [
        {'Issue key': 'AP-497'},
        {'Issue key': 'AP-433'},
    ]

def get_issue_changelog(issue_key):
    changelog = None

    try:
        with open('{}/{}.json'.format(CACHE_DIR, issue_key), 'r') as _file:
            changelog = json.loads(_file.read())
    except:
        print('No cache for {}, fetching from API'.format(issue_key))
        changelog = get_issue_changelog_from_api(issue_key)
        if changelog is not None:
            with open('{}/{}.json'.format(CACHE_DIR, issue_key), 'w') as _file:
                _file.write(json.dumps(changelog, indent=4, sort_keys=True))

    return changelog

def get_issue_changelog_from_api(issue_key):
    changelog = None
    res = session.get(BASE_URL + f'issue/{issue_key}/changelog', params={'maxResults': 1000})
    if res.status_code == 200:
        changelog = json.loads(res.content)
        if changelog.get('isLast') == False:
            print(issue_key + ' has more than 1000 changelogs')
    else:
        print('Failed to fetch {}. Reason: {} {}'.format(issue_key, res.status_code, res.content))
    return changelog

def get_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')

def parse_start_and_end_dates(issue_changelog):
    first_in_progress = None
    last_in_progress = None
    done_date = None

    for val in issue_changelog.get('values', []):
        for item in val.get('items', []):
            if item['field'] == 'status':
                cur_date = get_date(val['created'])
                if item['fromString'] == 'To Do' and item['toString'] in ['In Progress', 'In Review', 'Done']:
                    if not first_in_progress:
                        first_in_progress = cur_date
                    if not last_in_progress:
                        last_in_progress = cur_date
                    if cur_date < first_in_progress:
                        first_in_progress = cur_date
                    if cur_date > last_in_progress:
                        last_in_progress = cur_date
                if item['toString'] == 'Done':
                    if not done_date:
                        done_date = cur_date
                    if cur_date > done_date:
                        done_date = cur_date

    return {
        'First In Progress': first_in_progress,
        'Last In Progress': last_in_progress,
        'Done': done_date,
    }

def compute_cycle_time(start, end):
    day_generator = (start + timedelta(x + 1) for x in range((end - start).days + 1))
    days = sum(1 for day in day_generator if day.weekday() < 5)
    return days

# issues = get_issue_list_from_hard_coded()
issues = get_issue_list_from_csv()

for issue in issues:
    changelog = get_issue_changelog(issue['Issue key'])
    dates = parse_start_and_end_dates(changelog)
    issue.update(dates)
    issue.update({
        'Cycle Time (F)': compute_cycle_time(dates['First In Progress'], dates['Done']),
        'Cycle Time (L)': compute_cycle_time(dates['Last In Progress'], dates['Done']),
    })

with open('jira-with-cycle-times.csv', 'w') as _file:
    csv_file = csv.DictWriter(_file, fieldnames=csv_headers)
    csv_file.writeheader()
    csv_file.writerows(issues)
