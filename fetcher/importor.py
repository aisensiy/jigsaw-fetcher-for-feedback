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
    r = session.post(API_PREFIX + '/authentication/native',
                     json={'user_name': bg_user_name, 'user_password': bg_password})
    print 'login get status', r.status_code
    if r.status_code != 200:
        sys.exit(1)
    return session


def get_role(role, grade):
    if grade in ['Lead Con', 'Prin Con'] and role in ['Dev']:
        return "STACK_MANAGER"

    if role in ['BA', 'Mgr', 'CP', 'Head', 'PM']:
        return "PM"

    return "DEV"


def import_users(session, peoples):
    for idx, row in peoples.iterrows():
        id = row['employeeId']
        name = row['loginName']
        role = get_role(row['role'], row['grade'])
        r = session.get(API_PREFIX + '/users/' + str(id))
        if r.status_code == 200:
            continue
        r = session.post(API_PREFIX + '/users',
                         json={'id': id, 'name': name, 'role': role, 'email': name + '@thoughtworks.com', 'password': name})
        if r.status_code == 201:
            print 'import', str(id), str(name)
        else:
            print 'failed for import user', str(name)


def date_format(date):
    splits = date.split("-")
    return "-".join(reversed(splits))


def import_assignments(session, assignments):
    processed = set()
    for idx, row in assignments.iterrows():
        project_id = row['projectId']
        project_name = row['projectName']
        employee_id = row['employeeId']
        project_account = row['account']

        r = session.get(API_PREFIX + '/projects/' + str(project_id))
        print r.status_code
        if r.status_code == 404:
            url = API_PREFIX + '/projects'
            r = session.post(API_PREFIX + '/projects',
                             json={'id': project_id,
                                   'name': project_name,
                                   'account': project_account
                                   })
            print 'create project', url, r.status_code
        if project_id not in processed:
            url = '%s/projects/%d/members' % (API_PREFIX, project_id)
            r = session.delete(url)
            print 'clean project %d members %d' % (project_id, r.status_code)
            processed.add(project_id)
        url = '%s/projects/%d/members' % (API_PREFIX, project_id)

        r = session.post(url,
                         json={'user': employee_id})
        print 'post', url, r.status_code


def main():
    session = login()
    peoples = pd.read_csv('peoples.csv', encoding='utf8')
    import_users(session, peoples)
    assignments = pd.read_csv('assignments.csv', encoding='utf8')
    import_assignments(session, assignments)


if __name__ == '__main__':
    main()
