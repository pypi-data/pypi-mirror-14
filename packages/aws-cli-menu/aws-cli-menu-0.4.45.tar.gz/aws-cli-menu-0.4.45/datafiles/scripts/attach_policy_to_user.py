#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    menu = get_iam_users(session)

    if len(menu) > 0:
        print("\n")
        print("#######################")
        print("Users")
        print("#######################")
        print_user_menu(menu)
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        print"\n\n"
        user_name = menu[int(ans)][0]

        response = client.list_policies(
            Scope='Local'
        )

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

            response = client.attach_user_policy(
                UserName=user_name,
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
        print("###################")
        print('No users found')
        print("###################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
