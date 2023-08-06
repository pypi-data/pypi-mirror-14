#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_instances()

    if 'DBInstances' in response:
        stacks = response['DBInstances']

        if len(stacks) > 0:

            menu = {}
            counter =0
            for s in stacks:
                print(pretty(s))
                counter +=1
                my_list = []
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s['Engine'])
                menu[counter]=my_list

            print "\n\n"
            print '#########################################'
            print '## Select Instance To Snapshot         ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:

                        instance_id = menu[int(ans)][0]
                        break

            snapshot_id = raw_input("Enter Snapshot ID (example: my-snapshot-id): [ENTER]")

            response = client.create_db_snapshot(
                DBSnapshotIdentifier=snapshot_id,
                DBInstanceIdentifier=instance_id
            )

            print("\n")
            print(pretty(response))
            
        else:
            print("\n")
            print("####################")
            print('No RDS Instances')
            print("####################")
    else:
        print("\n")
        print("#####################")
        print('No RDS Instances')
        print("#####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
