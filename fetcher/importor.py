#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import requests
import sys
import config

API_PREFIX = config.KETSU_ENTRYPOINT
bg_user_name = config.KETSU_USERNAME
bg_password = config.KETSU_PASSWORD


def login():
    session = requests.Session()
    r = session.post(API_PREFIX + '/authentication',
                     json={'username': bg_user_name, 'password': bg_password})
    print 'login get status', r.status_code
    if r.status_code != 200:
        sys.exit(1)
    return session


def get_type(department):
    if department.lower().startswith('people'):
        return 'SYSTEM_ADMIN'
    else:
        return "NORMAL"


def import_users(session, peoples):
    for idx, row in peoples.iterrows():
        id = row['employeeId']
        username = row['loginName']
        nickname = row['preferredName']
        email = username + '@thoughtworks.com'
        role = row['role']
        grade = row['grade']
        userType = get_type(row['department'])
        home_office = row['home_office']
        department = row['department']
        password = username
        r = session.get(API_PREFIX + '/users/' + str(id))
        if r.status_code == 200:
            continue
        r = session.post(API_PREFIX + '/users',
                         json={'id': id,
                               'username': username,
                               'nickname': nickname,
                               'email': email,
                               'role': role,
                               'grade': grade,
                               'type': userType,
                               'home_office': home_office,
                               'password': password,
                               'department': department
                               })
        if r.status_code == 201:
            print 'import', str(id), str(username)
        else:
            print 'failed for import user', str(username)


def date_format(date):
    splits = date.split("-")
    return "-".join(reversed(splits))


def main():
    session = login()
    peoples = pd.read_csv('peoples.csv', encoding='utf8')
    import_users(session, peoples)


if __name__ == '__main__':
    main()
