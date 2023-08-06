#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_event_subscriptions()

    if 'EventSubscriptionsList' in response:
        stacks = response.get('EventSubscriptionsList')

        if len(stacks) > 0:
            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['SnsTopicArn'])
                my_list.append(s['Status'])
                my_list.append(s)
                menu[counter]=my_list


            print('#######################')
            print('Select Event Subscription')
            print('#######################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][2]
                        break

            print("\n")
            print("##################################")
            print("Detailed Event Subscription Info")
            print("##################################")
            print(pretty(info))

        else:
            print("\n")
            print("###########################")
            print("No Event Subscriptions")
            print("###########################")
    else:
        print("\n")
        print("############################")
        print('No Event Subscriptions')
        print("############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
