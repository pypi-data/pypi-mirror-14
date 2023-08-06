#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    response = client.list_roles()

    if 'Roles' in response:

        stacks = response.get('Roles')

        if len(stacks) > 0:

            menu = {}
            fields = {}

            for s in stacks:
                list = []
                name = str(s.get('RoleName'))
                id = str(s.get('RoleId'))
                list.append(name)
                list.append(id)
                fields[name] = list

            counter = 0
            for item in sorted(fields):
                counter = counter + 1
                menu[counter] = fields[item]

            #menu = get_iam_roles(session)

            if len(menu) > 0:
                print_role_menu(menu)

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            role_name = menu[int(ans)][0]
                            break

                response = client.list_attached_role_policies(
                    RoleName=role_name,
                )

                if 'AttachedPolicies' in response:

                    stacks = response['AttachedPolicies']

                    if len(stacks) > 0:

                        for i in stacks:
                            print("###################")
                            print("Policy")
                            print("###################")

                            print(pretty(i))
                    else:
                        print("\n")
                        print("#############################################")
                        print("Role does not have any attached policies")
                        print("#############################################")

                else:
                    print("\n")
                    print("#############################################")
                    print("Role does not have any attached policies")
                    print("#############################################")

            else:
                print("\n")
                print("#########################")
                print("No Roles Found")
                print("#########################")

        else:
            print("\n")
            print("#########################")
            print("No Roles Found")
            print("#########################")

    else:
        print ("\n")
        print '#############################'
        print '## No Roles Found          ##'
        print '#############################'

except (KeyboardInterrupt, SystemExit):
    sys.exit()
