#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')

    print("\n")
    name = raw_input("Enter new placement group name: [ENTER]")

    response = client.create_placement_group(
        DryRun=False,
        GroupName=name,
        Strategy='cluster'
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
