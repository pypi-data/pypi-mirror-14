#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('autoscaling')

    response = client.describe_auto_scaling_groups()

    if 'AutoScalingGroups' in response:
        stacks = response.get('AutoScalingGroups')

        if len(stacks) > 0:
            for s in stacks:
                name = s.get('AutoScalingGroupARN')
                print('#######################')
                print('AutoScalingGroups name: ' + str(name))
                print('#######################')
                print(pretty(s))
        else:
            print("\n")
            print("#########################")
            print('No AutoScalingGroups')
            print("#########################")
    else:
        print("\n")
        print("##########################")
        print('No AutoScalingGroups')
        print("##########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
