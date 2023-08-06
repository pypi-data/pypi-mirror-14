#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')
    response = client.list_groups()
    stacks = response.get('Groups')

    if len(stacks) > 0:  # There are groups

        group_menu = {}
        group_fields = {}

        for s in stacks:

            group_list = []
            group_name = str(s.get('GroupName'))
            group_list.append(group_name)

            group_fields[group_name] = group_list

        counter = 0
        for item in sorted(group_fields):
            counter = counter + 1
            group_menu[counter] = group_fields[item]

        print("\n")
        print('#######################')
        print('Groups')
        print('#######################')

        for key in sorted(group_menu):
            print str(key) + ":" + group_menu[key][0]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in group_menu:
                    group_name = group_menu[int(ans)][0]
                    break

        print"\n"

        response = client.list_attached_group_policies(
            GroupName=group_name
        )

        attached_policies = response['AttachedPolicies']

        if len(attached_policies) > 0:
            policy_menu = {}
            policy_fields = {}

            for s in attached_policies:
                policy_list = []
                name = str(s.get('PolicyName'))
                arn = str(s.get('PolicyArn'))
                policy_list.append(name)
                policy_list.append(arn)
                policy_fields[name] = policy_list

            counter = 0
            for item in sorted(policy_fields):
                print('item: ' + str(item))
                counter = counter + 1
                policy_menu[counter] = policy_fields[item]

            print("\n")
            print('#######################')
            print('Policies')
            print('#######################')

            for key in sorted(policy_menu):
                print str(key) + ":" + policy_menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in policy_menu:

                        arn = policy_menu[int(ans)][1]
                        break

            print"\n"

            response = client.detach_group_policy(
                GroupName=group_name,
                PolicyArn=arn
            )
            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("########################")
            print('There are no policies')
            print("########################")
    else:
        print("\n")
        print("########################")
        print('There are no groups.')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
