#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_addresses(
        DryRun=False
    )

    if 'Addresses' in response:

        stacks = response['Addresses']
        for i in stacks:
            print("###############")
            print("Address")
            print("###############")
            print(pretty(i))

    else:
        print("\n")
        print("################")
        print("No Addresses")
        print("################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
