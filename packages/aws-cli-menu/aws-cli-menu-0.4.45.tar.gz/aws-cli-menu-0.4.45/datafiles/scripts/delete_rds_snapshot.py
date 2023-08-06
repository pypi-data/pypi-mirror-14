#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_snapshots()

    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:

            menu = {}
            counter =0
            for s in stacks:
                counter +=1
                my_list = []
                my_list.append(s.get('DBInstanceIdentifier'))
                my_list.append(s.get('DBSnapshotIdentifier'))
                my_list.append(s['Engine'])
                menu[counter]=my_list

            print "\n\n"
            print '#########################################'
            print '## Select Snapshot To Delete           ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        snapshot_id = menu[int(ans)][1]
                        break

            response = client.delete_db_snapshot(
                DBSnapshotIdentifier=snapshot_id
            )
            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("####################")
            print('No RDS Snapshots')
            print("####################")
    else:
        print("\n")
        print("#####################")
        print('No RDS Snapshots')
        print("#####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
