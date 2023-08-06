#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('autoscaling')

    response = client.describe_launch_configurations()

    if 'LaunchConfigurations' in response:
        stacks = response.get('LaunchConfigurations')

        if len(stacks) > 0:
            for s in stacks:
                print("\n")
                print('###########################')
                print('LaunchConfigurations')
                print('###########################')
                print(pretty(s))
        else:
            print("\n")
            print("#############################")
            print('No LaunchConfigurations')
            print("#############################")
    else:
        print("\n")
        print("#############################")
        print('No LaunchConfigurations')
        print("#############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
