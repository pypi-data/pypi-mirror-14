#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')
    response = client.list_policies(
        Scope='Local'
    )

    stacks = response.get('Policies')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for i in stacks:
            counter += 1
            my_list = []
            my_list.append(i['PolicyName'])
            my_list.append(i['Arn'])
            menu[counter] = my_list

        print "\n"
        print '#########################################'
        print '## Select Policty To Delete            ##'
        print '########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    arn = menu[int(ans)][1]
                    break

        print"\n"
        response = client.delete_policy(
            PolicyArn=arn
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("###########################################")
        print('There are no customer managed policies.')
        print("###########################################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
