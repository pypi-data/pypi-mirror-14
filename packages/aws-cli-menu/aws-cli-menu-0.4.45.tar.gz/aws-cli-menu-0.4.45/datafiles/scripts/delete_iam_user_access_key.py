#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    menu = get_iam_users(session)

    if len(menu) > 0:

        print("\n")
        print("#################################")
        print("Select User")
        print("#################################")

        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    user_name = menu[int(ans)][0]
                    break

        client = session.client('iam')
        response = client.list_access_keys(
            UserName=user_name
            # Marker='string',
            # MaxItems=123
        )

        if 'AccessKeyMetadata' in response:

            stack = response['AccessKeyMetadata']
            if len(stack) > 0:

                menu = {}
                counter = 0
                for i in stack:

                    counter += 1
                    my_list = []
                    my_list.append(i['AccessKeyId'])
                    my_list.append(i['Status'])
                    menu[counter] = my_list

                print("\n")
                print("#################################")
                print("Select Access Key To Delete")
                print("#################################")

                for key in sorted(menu):
                    print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            key_id = menu[int(ans)][0]
                            break

                response = client.delete_access_key(
                    UserName=user_name,
                    AccessKeyId=key_id
                )

                print("\n")
                print(pretty(response))

            else:
                print("\n")
                print("#############################################")
                print("User does not have any access keys.")
                print("#############################################")
        else:
            print("\n")
            print("#############################################")
            print("User does not have any access keys.")
            print("#############################################")

    else:
        print("\n")
        print("####################")
        print('No users found')
        print("####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
