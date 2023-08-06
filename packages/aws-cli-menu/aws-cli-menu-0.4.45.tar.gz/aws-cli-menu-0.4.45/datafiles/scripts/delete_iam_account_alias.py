#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    response = client.list_account_aliases()


    if 'AccountAliases' in response:

        stacks = response.get('AccountAliases')

        if len(stacks)>0:

            print("\n")
            print("####################################")
            print("Select Account Aliases To Delete")
            print("####################################")

            menu = {}
            counter =0
            for i in stacks:
                counter+= 1
                menu[counter]=i

            for key in sorted(menu):
                print(str(key) + ":" + menu[key])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        name = menu[int(ans)]
                        break

            response = client.delete_account_alias(
                AccountAlias=name
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##############")
            print("No Aliases")
            print("##############")
    else:
        print("\n")
        print("######################")
        print("No Aliases")
        print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
