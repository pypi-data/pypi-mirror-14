#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')



    type = [
        'cache-cluster',
        'cache-parameter-group',
        'cache-security-group',
        'cache-subnet-group'
    ]

    menu = {}
    counter=0
    for i in sorted(type):
        counter+=1
        menu[counter]=i

    print "\n"
    print '#########################################'
    print '## Select Event Type'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                event_type = menu[int(ans)]
                break

    response = client.describe_events(
        SourceType=event_type
    )


    if 'Events' in response:

        stacks = response['Events']

        if len(stacks):

            menu = {}
            counter=0
            for i in stacks:
                counter+=1
                my_list=[]
                my_list.append(i['Message'])
                my_list.append(i)
                menu[counter]=my_list

            print "\n"
            print '#########################################'
            print '## Select Cache Event'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][1]
                        break

            print("\n")
            print("#####################################")
            print("Detailed Cache Event")
            print("#####################################")
            print(pretty(info))

        else:
            print("\n")
            print("##################################")
            print("No Cache Events")
            print("##################################")

    else:
        print("\n")
        print("##################################")
        print("No Cache Events")
        print("##################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
