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
    url = "https://jigsaw.thoughtworks.net/api/people.json"
    querystring = {"home_office": office}
    headers = {
        'authorization': JIGSAW_TOKEN,
        'cache-control': "no-cache"
    }

    response = fetch(url, headers, querystring)

    if response.status_code == 200:
        peoples = response.json()
        total = int(response.headers.get('x-total-pages'))
        total_count = int(response.headers.get('x-total-count'))
        print 'total page', str(total)
        print 'total count', str(total_count)
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
    header = ['employeeId', 'loginName', 'preferredName', 'role', 'grade', 'department', 'home_office', 'avatarUrl']
    result = []
    for people in peoples:
        result.append([
            people['employeeId'],
            people['loginName'],
            people['preferredName'],
            people['role']['name'],
            people['grade']['name'],
            people['department']['name'],
            people['homeOffice']['name'],
            people['picture']['url']
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

if __name__ == "__main__":
    main()