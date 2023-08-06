#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('autoscaling')

    response = client.describe_auto_scaling_instances()

    if 'AutoScalingInstances' in response:
        stacks = response.get('AutoScalingInstances')

        if len(stacks) > 0:
            for s in stacks:
                name = s.get('AutoScalingInstanceARN')
                print('#######################')
                print('AutoScalingInstances name: ' + str(name))
                print('#######################')
                print(pretty(s))
        else:
            print("\n")
            print("############################")
            print('No AutoScalingInstances')
            print("############################")
    else:
        print("\n")
        print("############################")
        print('No AutoScalingInstances')
        print("############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
