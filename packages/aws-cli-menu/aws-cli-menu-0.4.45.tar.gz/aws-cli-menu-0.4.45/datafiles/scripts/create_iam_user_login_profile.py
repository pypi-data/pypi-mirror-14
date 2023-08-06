#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re
from botocore.client import ClientError

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

        try:
            client = session.client('iam')
            response = client.get_login_profile(
                UserName=user_name
            )

            print(pretty(response))
            if 'LoginProfile' in response:

                stack = response['LoginProfile']
                if len(stack) > 0:

                    print("\n")
                    print("########################################")
                    print("User Already Has A Login Profile Of")
                    print("########################################")
                    print(pretty(stack))
                else:
                    print("\n")
                    print("#############################################")
                    print("User does not have any login profile.")
                    print("#############################################")
            else:
                print("\n")
                print("#############################################")
                print("User does not have any login profile.")
                print("#############################################")

        except ClientError as e:
            print(generate_password())

            response = client.create_login_profile(
                UserName=user_name,
                Password=generate_password(),
                PasswordResetRequired=True
            )

            print("\n")
            print(pretty(response))

    else:
        print("\n")
        print("####################")
        print('No users found')
        print("####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
