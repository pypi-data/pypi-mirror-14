#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    snapshot_name = raw_input('Enter the name of the snapshot you are searching for :')

    response = client.describe_db_snapshots(
        DBSnapshotIdentifier=snapshot_name,
    )

    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:

            if stacks[0]['Status'] == 'available':
                print("\n")
                print("########################################")
                print('Found RDS Snapshot - '+snapshot_name+' and it is available')
                print("########################################")
            else:
                print("\n")
                print("########################################")
                print('Found RDS Snapshot - '+snapshot_name+' but it is unavailable')
                print("########################################")


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
