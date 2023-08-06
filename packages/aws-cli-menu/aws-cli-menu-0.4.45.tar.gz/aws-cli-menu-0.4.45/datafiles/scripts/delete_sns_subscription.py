#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('sns')

    response = client.list_subscriptions()

    if 'Subscriptions' in response:
        stacks = response.get('Subscriptions')

        if len(stacks) > 0:

            menu = {}
            counter = 0
            for s in stacks:
                counter += 1
                my_list = []
                my_list.append(s['TopicArn'])
                my_list.append(s['SubscriptionArn'])
                menu[counter] = my_list

            print "\n\n"
            print '#########################################'
            print '## Select Subscription to Delete       ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:

                    if int(ans) in menu:
                        arn = menu[int(ans)][1]
                        break

            response = client.unsubscribe(
                SubscriptionArn=arn
            )

            print("\n")
            print(pretty(response))

        else:
            print("########################")
            print('No SQS Subscriptions')
            print("########################")

    else:
        print("########################")
        print('No SQS Subscriptions')
        print("########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
