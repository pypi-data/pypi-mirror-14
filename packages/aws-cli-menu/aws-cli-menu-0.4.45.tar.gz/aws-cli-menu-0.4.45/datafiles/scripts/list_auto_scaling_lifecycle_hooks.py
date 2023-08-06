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

            menu = {}
            names = []

            for s in stacks:
                name = s.get('AutoScalingGroupName')
                names.append(name)

            counter = 0
            for item in sorted(names):
                counter = counter + 1
                menu[counter] = item

            if len(menu) > 0:

                print "\n\n"
                print '#########################################'
                print '## Auto Scaling Groups                 ##'
                print '#########################################'
                for key in sorted(menu):
                    print(str(key) + ":" + menu[key])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        asg_name = menu[int(ans)]
                        break

            response = client.describe_lifecycle_hooks(
                AutoScalingGroupName=asg_name,

            )

            if 'LifecycleHooks' in response:
                stacks = response.get('LifecycleHooks')

                if len(stacks) > 0:
                    for s in stacks:
                        print("\n")
                        print('###########################')
                        print('LifecycleHooks')
                        print('###########################')
                        print(pretty(s))

                else:
                    print("\n")
                    print("###################################")
                    print('No Auto Scaling Lifecycle Hooks')
                    print("###################################")
            else:
                print("\n")
                print("###################################")
                print('No Auto Scaling Lifecycle Hooks')
                print("###################################")

        else:
            print("\n")
            print("############################")
            print('No Auto Scaling Groups')
            print("############################")
    else:
        print("\n")
        print("############################")
        print('No Auto Scaling Groups')
        print("############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
