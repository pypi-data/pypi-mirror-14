#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    response = client.create_internet_gateway(
        DryRun=False
    )

    print("\n")
    print("########################")
    print("New Internet Gateway")
    print("########################")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
