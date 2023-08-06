#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_security_groups()
    stacks = response.get('SecurityGroups')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for s in stacks:
            counter += 1
            my_list = []
            my_list.append(s['GroupName'])
            my_list.append(s['Description'])
            my_list.append(s)
            menu[counter] = my_list

        print "\n"
        print '#########################################'
        print '## Select Security Group               ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    answer = menu[int(ans)][2]
                    break

        print("\n")
        print("######################################")
        print("Detailed Security Group Information")
        print("######################################")

        print(pretty(answer))
    else:
        print("\n")
        print("##############################")
        print('No security groups found')
        print("##############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
