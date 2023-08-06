#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    id = select_snapshot_id(session)

    client = session.client('ec2')

    response = client.delete_snapshot(
        DryRun=False,
        SnapshotId=id
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
