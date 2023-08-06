#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('sqs')

    response = client.list_queues()

    if 'QueueUrls' in response:
        stacks = response.get('QueueUrls')

        if len(stacks) > 0:

            menu = {}
            counter = 0
            for s in stacks:
                counter += 1
                menu[counter] = s

            print "\n"
            print '#########################################'
            print '## Select SQS Queue To Delete          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        url = menu[int(ans)]
                        break

            response = client.delete_queue(
                QueueUrl=url
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##################")
            print('No SQS Queues')
            print("##################")
    else:
        print("\n")
        print("####################")
        print('No SQS Queues')
        print("####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
