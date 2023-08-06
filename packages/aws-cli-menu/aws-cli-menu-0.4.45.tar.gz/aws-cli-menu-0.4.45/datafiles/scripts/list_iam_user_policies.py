#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')

    response = client.list_users()
    stacks = response.get('Users')

    menu = {}
    fields = {}

    if len(stacks) > 0:
        for s in stacks:
            list = []
            name = str(s.get('UserName'))
            id = str(s.get('UserId'))
            list.append(name)
            list.append(id)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter + 1
            menu[counter] = fields[item]

        print("\n")
        print('#######################')
        print('Users')
        print('#######################')
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    user_name = menu[int(ans)][0]
                    break

        print"\n"

        response = client.list_user_policies(
            UserName=user_name
        )

        if 'PolicyNames' in response:

            stacks = response['PolicyNames']

            if len(stacks)>0:

                for i in stacks:

                    print("############")
                    print("Policy")
                    print("############")
                    print(pretty(i))

            else:
                print("\n")
                print("######################")
                print("User Has No Policies")
                print("######################")

        else:
            print("\n")
            print("######################")
            print("User Has No Policies")
            print("######################")
    else:
        print("\n")
        print("##################################################")
        print('No users listed. Need at least one user defined.')
        print("##################################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
