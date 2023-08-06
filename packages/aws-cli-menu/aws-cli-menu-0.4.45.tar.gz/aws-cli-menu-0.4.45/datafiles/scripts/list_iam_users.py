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
        response = client.get_user(UserName=str(user_name))
        user_info = response.get('User')

        print "\n\n"
        print '#############################'
        print '## User Info               ##'
        print '#############################'

        print(pretty(user_info))

    else:
        print("\n")
        print("####################")
        print('No users found')
        print("####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
