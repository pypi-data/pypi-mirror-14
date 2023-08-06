#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_instances()

    menu = {}

    if 'DBInstances' in response:
        stacks = response.get('DBInstances')

        if len(stacks) > 0:
            counter = 0
            for s in stacks:
                counter += 1
                name = s.get('DBName')
                identifier = s.get('DBInstanceIdentifier')
                print('#######################')
                print('Database name: ' + str(name))
                print('#######################')
                my_list = []
                my_list.append(name)
                my_list.append(identifier)
                menu[counter] = my_list

            print "\n\n"
            print '#########################################'
            print '## RDS Instances                       ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        rds_id = menu[int(ans)][1]
                        break

            print"\n"

            response = client.describe_db_snapshots(
                DBInstanceIdentifier=rds_id,
            )

            stacks = response.get('DBSnapshots')[-1]
            snapshot_id = stacks['DBSnapshotIdentifier']
            print('snapshot id: ' + str(snapshot_id))

            matchObj = re.match(r'rds:(.*)', snapshot_id, re.M | re.I)

            if matchObj:

                response = client.delete_db_instance(
                    DBInstanceIdentifier=rds_id,
                    FinalDBSnapshotIdentifier=matchObj.group(1)
                )

                print("\n")
                print("#############################")
                print("Deleting Instance")
                print("#############################")

                print(pretty(response))

        else:
            print("\n")
            print("####################")
            print('No RDS Instances')
            print("#####################")
    else:
        print("\n")
        print("#####################")
        print('No RDS Instances')
        print("#####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
