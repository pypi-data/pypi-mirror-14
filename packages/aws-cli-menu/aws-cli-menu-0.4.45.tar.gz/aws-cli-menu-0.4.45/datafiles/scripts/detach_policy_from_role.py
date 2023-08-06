#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    menu = get_iam_roles(session)

    if len(menu) > 0:
        print_role_menu(menu)
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        print"\n"
        role_name = menu[int(ans)][0]

        print"\n"

        response = client.list_attached_role_policies(
            RoleName=role_name
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
                #print('item: '+str(item))
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

            response = client.detach_role_policy(
                RoleName=role_name,
                PolicyArn=arn
            )

            if 'ResponseMetadata' in response:
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    print("\n")
                    print("######################################")
                    print("Policy has been detached from role.")
                    print("######################################")
                else:
                    print("\n")
                    print(pretty(response))

            else:
                print("\n")
                print(pretty(response))

        else:
            print("\n")
            print("#########################")
            print('There are no policies')
            print("#########################")
    else:
        print "\n\n"
        print '#############################'
        print '## Role Info               ##'
        print '#############################'
        print('No roles found')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
