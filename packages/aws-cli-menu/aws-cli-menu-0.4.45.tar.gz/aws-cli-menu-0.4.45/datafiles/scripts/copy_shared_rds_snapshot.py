#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    source_rds_snapshot_name  = raw_input('Enter the name of the source RDS snapshot name: ')

    target_rds_snapshot_name = raw_input('Enter the name of the target RDS snapshot name: ')



    #response = client.copy_db_snapshot(
    #    SourceDBSnapshotIdentifier=str(source_rcs_snapshot_name),
    #    TargetDBSnapshotIdentifier=str(target_rds_snapshot_name),
    #    CopyTags=False
    #)

    #print(pretty(response))



except (KeyboardInterrupt, SystemExit):
    sys.exit()
