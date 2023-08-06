#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('sns')

    response = client.list_topics()

    if 'Topics' in response:
        stacks = response.get('Topics')

        if len(stacks) > 0:

            for s in stacks:
                print("#############")
                print("Topic")
                print("#############")
                print(pretty(s))

        else:
            print("\n")
            print("###################")
            print('No SQS Topics')
            print("###################")
    else:
        print("\n")
        print("##################")
        print('No SQS Topics')
        print("##################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
