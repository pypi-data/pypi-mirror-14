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

        print"\n\n"

        response = client.list_policies()
        stacks = response.get('Policies')

        if len(stacks) > 0:
            menu = {}
            fields = {}

            for s in stacks:
                list = []
                name = str(s.get('PolicyName'))
                arn = str(s.get('Arn'))
                list.append(name)
                list.append(arn)
                fields[name] = list

            counter = 0
            for item in sorted(fields):
                counter = counter + 1
                menu[counter] = fields[item]

            print("\n")
            print('#######################')
            print('Policies')
            print('#######################')

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        arn = menu[int(ans)][1]
                        break

            print"\n\n"

            response = client.attach_group_policy(
                GroupName=group_name,
                PolicyArn=arn
            )

            print(pretty(response))

        else:
            print("\n")
            print("#########################")
            print('There are no policies')
            print("#########################")
    else:
        print("\n")
        print("########################")
        print('There are no groups.')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
