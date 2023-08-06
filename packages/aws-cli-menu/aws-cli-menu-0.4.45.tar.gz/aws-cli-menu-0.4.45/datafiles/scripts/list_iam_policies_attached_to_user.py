#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    menu = get_iam_users(session)

    if len(menu) > 0:
        print("\n")
        print("#######################")
        print("Users")
        print("#######################")
        print_user_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        user_name = menu[int(ans)][0]

        client = session.client('iam')

        response = client.list_attached_user_policies(
            UserName=user_name
        )

        if 'AttachedPolicies' in response:
            policies = response.get('AttachedPolicies')

            if len(policies) > 0:
                print "\n"
                print '#############################'
                print '## User Policies               ##'
                print '#############################'

                print(pretty(policies))

            else:
                print("\n")
                print"############################################"
                print("User does not have any attached policies")
                print"############################################"

        else:
            print("\n")
            print"############################################"
            print("User does not have any attached policies")
            print"############################################"
    else:
        print("\n")
        print("####################")
        print('No users found')
        print("####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
