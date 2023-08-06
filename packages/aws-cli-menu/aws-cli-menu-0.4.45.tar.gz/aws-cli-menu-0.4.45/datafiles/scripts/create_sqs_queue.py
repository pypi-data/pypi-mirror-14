#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('sqs')

    print("\n")
    name = raw_input("Enter name for new queue. [ENTER]")

    response = client.create_queue(
        QueueName=name
        # Attributes={
        #    'string': 'string'
        #}
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
