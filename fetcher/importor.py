#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import requests
import sys
import config

API_PREFIX = config.FEEDBACK_ENTRYPOINT
bg_user_name = config.FEEDBACK_USERNAME
bg_password = config.FEEDBACK_PASSWORD


def login():
    session = requests.Session()
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


def import_users(session, peoples):
    for idx, row in peoples.iterrows():
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
            'department': (row['department'])
        }

        r = session.get(API_PREFIX + '/users/' + str(row['employeeId']))
        if r.status_code == 200:
            r = session.put(API_PREFIX + '/users/' + str(row['employeeId']), json=data)
        else:
            r = session.post(API_PREFIX + '/users', json=data)
        if r.status_code == 201 or r.status_code == 204:
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
