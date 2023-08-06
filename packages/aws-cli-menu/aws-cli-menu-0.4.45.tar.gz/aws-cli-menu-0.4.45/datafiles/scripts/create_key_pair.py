#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    keypair_name = raw_input("Enter key pair name: [ENTER]")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.create_key_pair(
        DryRun=False,
        KeyName=keypair_name
    )

    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
