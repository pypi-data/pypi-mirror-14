#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')
    response = client.list_groups()

    stacks = response.get('Groups')

    print("\n")

    if len(stacks) > 0:
        for s in stacks:
            print("###################")
            print("Group - " + str(s['GroupName']))
            print("###################")

            print(pretty(s))

    else:
        print("\n")
        print("##########################")
        print("There are no groups.")
        print("##########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
