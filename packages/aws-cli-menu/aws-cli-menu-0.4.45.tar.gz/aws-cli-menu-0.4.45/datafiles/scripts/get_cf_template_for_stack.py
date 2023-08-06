#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('cloudformation')
    response = client.list_stacks(
        StackStatusFilter=[
            'CREATE_IN_PROGRESS',
            'CREATE_FAILED',
            'CREATE_COMPLETE',
            'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
            'UPDATE_COMPLETE',
            'UPDATE_IN_PROGRESS'])
    stacks = response.get('StackSummaries')

    if len(stacks) > 0:
        dict = {}

        counter = 0
        menu = {}
        for s in stacks:
            counter += 1
            list = []
            list.append(s.get('StackName'))
            list.append(s.get('StackStatus'))
            menu[counter] = list

        print "\n\n"
        print '#########################################'
        print '## Select Stack                        ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    stack_name = menu[int(ans)][0]
                    break

        response = client.get_template(
            StackName=stack_name
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##############################")
        print('No undeleted stacks found')
        print("##############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
