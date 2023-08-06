#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    instance_name = raw_input("Enter RDS Instance Name: [ENTER]")
    instance_name = 'test'

    db_identifier = raw_input(
        "Enter DB Identifier (example: mydbinstance): [ENTER]")  # example: mydbinstance
    db_identifier = 'mydbinstance'

    engines = {
        1: 'MySQL',
        2: 'mariadb',
        3: 'oracle-se1',
        4: 'oracle-se',
        5: 'oracle-ee',
        6: 'sqlserver-ee',
        7: 'sqlserver-se',
        8: 'sqlserver-ex',
        9: 'sqlserver-web',
        10: 'postgres',
        11: 'aurora'
    }

    print "\n\n"
    print '#########################################'
    print '## Select Engine Type                  ##'
    print '#########################################'
    for key in sorted(engines):
        print str(key) + ":" + engines[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in engines:
                db_engine = engines[int(ans)]
                break

    print"\n"

    db_size = {
        1: 5,
        2: 10,
        3: 15,
        4: 20,
        5: 25,
        6: 30
    }

    print "\n\n"
    print '#########################################'
    print '## Select Database Size                ##'
    print '#########################################'
    for key in sorted(db_size):
        print str(key) + ":" + str(db_size[key])

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            #print('matches pattern')
            if int(ans) in db_size:
                #print('in profiles dictionary')
                size = db_size[int(ans)]
                break

    print"\n\n"

    types = {
        1: 'db.t1.micro',
        2: 'db.m1.small',
        3: 'db.m1.medium',
        4: 'db.m1.large',
        5: 'db.m1.xlarge',
        6: 'db.m2.xlarge',
        7: 'db.m2.2xlarge',
        8: 'db.m2.4xlarge',
        9: 'db.m3.medium',
        10: 'db.m3.large',
        11: 'db.m3.xlarge',
        12: 'db.m3.2xlarge',
        13: 'db.m4.large',
        14: 'db.m4.xlarge',
        15: 'db.m4.2xlarge',
        16: 'db.m4.4xlarge',
        17: 'db.m4.10xlarge',
        18: 'db.r3.large',
        19: 'db.r3.xlarge',
        20: 'db.r3.2xlarge',
        21: 'db.r3.4xlarge',
        22: 'db.r3.8xlarge',
        23: 'db.t2.micro',
        24: 'db.t2.small',
        25: 'db.t2.medium',
        26: 'db.t2.large'}

    print "\n"
    print '#########################################'
    print '## Select Database Type                ##'
    print '#########################################'
    for key in sorted(types):
        print str(key) + ":" + types[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in types:
                instance_type = types[int(ans)]
                break

    print"\n"

    username = raw_input("Enter DB username: [ENTER]")  # mysql_admin
    username = 'test'
    password = raw_input("Enter DB password: [ENTER]")  # 1nsecure
    password = '123456a!'

    response = client.create_db_instance(
        DBName=instance_name,
        DBInstanceIdentifier=db_identifier,
        AllocatedStorage=size,
        DBInstanceClass=instance_type,
        Engine=db_engine,
        MasterUsername=username,
        MasterUserPassword=password,

    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
