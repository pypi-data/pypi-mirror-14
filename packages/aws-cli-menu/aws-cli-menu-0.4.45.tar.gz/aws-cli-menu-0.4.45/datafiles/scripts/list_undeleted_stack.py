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

        for s in stacks:
            list = []
            list.append(s.get('StackName'))
            list.append(s.get('StackStatus'))
            dict[s.get('StackName')] = list

        print("\n\n")
        print('##################################')
        print('## Undeleted Stacks             ##')
        print('##################################')

        for key, value in sorted(dict.iteritems()):
            print("%s\t\t%s" % (value[0], value[1]))
    else:
        print("\n")
        print("#############################")
        print('No undeleted stacks found')
        print("#############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
