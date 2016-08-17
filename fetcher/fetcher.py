#!/usr/bin/env python
# encoding: utf-8

import requests
import pandas as pd
import time
import config
import sys

JIGSAW_TOKEN = config.JIGSAW_TOKEN

def fetch(url, headers, querystring):
    r = requests.request("GET", url, headers=headers, params=querystring, timeout=15)
    print 'get', r.url, r.status_code
    return r


def get_all_people_in_office(office='Beijing'):
    url = "https://jigsaw.thoughtworks.com/api/people.json"
    querystring = {"home_office": office}
    headers = {
        'authorization': JIGSAW_TOKEN,
        'cache-control': "no-cache"
    }

    response = fetch(url, headers, querystring)

    if response.status_code == 200:
        peoples = response.json()
        total = int(response.headers.get('x-total-pages'))
        print 'total page', str(total)
    else:
        print 'failed to get data'
        sys.exit(1)

    time.sleep(10)

    for page in range(2, total + 1):
        querystring['page'] = page
        response = fetch(url, headers, querystring)
        if response.status_code == 200:
            peoples += response.json()
        time.sleep(10)

    print 'len', len(peoples)
    return peoples


def people_to_csv(peoples, filename):
    header = ['employeeId', 'loginName', 'preferredName', 'role', 'grade', 'department', 'assignable']
    result = []
    for people in peoples:
        result.append([
            people['employeeId'],
            people['loginName'],
            people['preferredName'],
            people['role']['name'],
            people['grade']['name'],
            people['department']['name'],
            people['assignable']
        ])
    df = pd.DataFrame(result, columns=header)
    df.to_csv(filename, index=None, encoding='utf8')


def get_employee_assignment(ids):
    url = "https://jigsaw.thoughtworks.com/api/assignments.json"
    print 'get', url
    querystring = {"current_only": True, 'employee_ids[]': ids}
    headers = {
        'authorization': JIGSAW_TOKEN,
        'cache-control': "no-cache"
    }

    response = fetch(url, headers, querystring)
    assignments = response.json()
    return assignments


def fetch_assignments(ids):
    pagination = 10
    total = len(ids)
    assignments = []
    for i in range(0, total, pagination):
        assignments += get_employee_assignment(ids[i:i + pagination])
        time.sleep(10)
    return assignments


def assignment_to_csv(entities, filename):
    header = ['id', 'employeeId', 'account', 'projectId', 'projectName', 'startsOn', 'endsOn']
    result = []
    for entity in entities:
        result.append([
            entity['id'],
            entity['consultant']['employeeId'],
            entity['account']['name'],
            entity['project']['id'],
            entity['project']['name'],
            entity['duration']['startsOn'],
            entity['duration']['endsOn']
        ])
    df = pd.DataFrame(result, columns=header)
    df.to_csv(filename, index=None, encoding='utf8')


def main():
    offices = ['Beijing', 'Xi\'an', 'Chengdu', 'Shanghai', 'Wuhan', 'Shenzhen']
    peoples = []
    for office in offices:
        print office
        peoples += get_all_people_in_office(office)

    people_to_csv(peoples, 'peoples.csv')

    peoples = pd.read_csv('peoples.csv')
    ids = peoples['employeeId'].tolist()
    assignments = fetch_assignments(ids)
    assignment_to_csv(assignments, 'assignments.csv')
