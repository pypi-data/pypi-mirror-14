#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    snapshot_name = raw_input('Enter the name of the snapshot you are searching for :')

    response = client.describe_db_snapshots(
        #DBSnapshotIdentifier=snapshot_name,
        SnapshotType='shared',
        IncludeShared=True
    )

    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:

            for i in stacks:
                print(i['DBSnapshotIdentifier'])

                matchObj= re.match(r'(.*)'+str(snapshot_name)+'(.*)',i['DBSnapshotIdentifier'],re.M|re.I)

                if matchObj:
                   print "matchObj.group() : ", matchObj.group()
                   print "matchObj.group(1) : ", matchObj.group(1)
                   print "matchObj.group(2) : ", matchObj.group(2)
                else:
                   print "No match!!"

            print("\n")
            print("###################################################################")
            print(snapshot_name+' snapshot is shared with '+str(profile_name)+' account')
            print("###################################################################")


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
