#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import requests
import sys
import config
from requests.adapters import HTTPAdapter

API_PREFIX = config.FEEDBACK_ENTRYPOINT
bg_user_name = config.FEEDBACK_USERNAME
bg_password = config.FEEDBACK_PASSWORD


def login():
    session = requests.Session()
    session.mount(prefix="", adapter=HTTPAdapter(max_retries=5))
    r = session.post(API_PREFIX + '/authentication',
                     json={'username': bg_user_name, 'password': bg_password})
    print 'login get status', r.status_code
    if r.status_code not in [200, 201]:
        sys.exit(1)
    return session


def get_type(department):
    if department.lower().startswith('people'):
        return 'SYSTEM_ADMIN'
    else:
        return "NORMAL"


def user_equal(user1, user2):
    keys = ['img', 'role', 'nickname', 'department', 'type', 'email', 'username']
    for key in keys:
        if user1[key] != user2[key]:
            print '%s not equal %s != %s' % (key, str(user1[key]), str(user2[key]))
            return False
    return True


def import_users(session, peoples):
    for _, row in peoples.iterrows():
        data = {
            'id': (row['employeeId']),
            'username': (row['loginName']),
            'nickname': (row['preferredName']),
            'email': (row['loginName'] + '@thoughtworks.com'),
            'role': (row['role']),
            'grade': (row['grade']),
            'type': (get_type(row['department'])),
            'home_office': (row['home_office']),
            'password': (row['loginName']),
            'department': (row['department']),
            'img': row['avatarUrl']
        }

        r = session.get(API_PREFIX + '/users/' + str(row['loginName']))
        if r.status_code == 200 and not user_equal(r.json(), data):
            r = session.put(API_PREFIX + '/users/' + str(row['loginName']), json=data)
        elif r.status_code == 404:
            r = session.post(API_PREFIX + '/users', json=data)
        else:
            print 'skip', str(row['loginName'])
            continue

        if r.status_code == 201 or r.status_code == 204 or r.status_code == 200:
            print 'import', str(row['employeeId']), str(row['loginName'])
        else:
            print 'failed for import user', str(row['loginName'])


def date_format(date):
    splits = date.split("-")
    return "-".join(reversed(splits))


def main():
    session = login()
    peoples = pd.read_csv('peoples.csv', encoding='utf8')
    import_users(session, peoples)


if __name__ == '__main__':
    main()
