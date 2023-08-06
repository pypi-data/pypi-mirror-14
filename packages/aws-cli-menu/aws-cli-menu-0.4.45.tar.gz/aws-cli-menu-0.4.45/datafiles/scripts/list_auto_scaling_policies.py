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

                response = client.describe_policies(
                    AutoScalingGroupName=asg_name,
                    MaxRecords=25
                )
                #print(response)

                if 'ScalingPolicies' in response:
                    stacks = response.get('ScalingPolicies')

                    if len(stacks) > 0:

                        menu = {}
                        counter =0
                        for s in stacks:
                            counter+=1
                            my_list = []
                            my_list.append(s['PolicyName'])
                            my_list.append(s)
                            menu[counter]=my_list

                        print("\n")
                        print '#########################################'
                        print '## Select Policy                       ##'
                        print '#########################################'
                        for key in sorted(menu):
                            print(str(key) + ":" + str(menu[key][0]))

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    info = menu[int(ans)][1]
                                    break

                        print("\n")
                        print('###########################')
                        print('Scaling Policy Details')
                        print('###########################')
                        print(pretty(info))

                    else:
                        print("\n")
                        print("#######################")
                        print('No ScalingPolicies')
                        print("#######################")
            else:
                print("\n")
                print("######################")
                print('No ScalingPolicies')
                print("######################")

        else:
            print("\n")
            print("########################")
            print('No Load Balancers')
            print("########################")
    else:
        print("\n")
        print("#######################")
        print('No Load Balancers')
        print("#######################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
