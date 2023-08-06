#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')

    response = client.describe_tags()

    stacks = response.get('Tags')

    resource_types = {}

    if len(stacks) > 0:

        for item in stacks:

            if item.get('ResourceType') in resource_types:
                resource_types[item.get('ResourceType')].append(item)
            else:
                resource_types[item.get('ResourceType')] = []
                resource_types[item.get('ResourceType')].append(item)

    menu = {}
    counter = 0
    for item in sorted(resource_types):
        counter += 1
        menu[counter] = item

    if len(menu) > 0:
        print "\n\n"
        print '#########################################'
        print '## Select Resource                     ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    resource_id = menu[int(ans)]
                    break

        print"\n\n"

        resources = resource_types[resource_id]

        print("\n")
        print("###############################")
        print(resource_id + " Tags")
        print("###############################")

        for item in resources:
            print(pretty(item))

    else:
        print("\n")
        print("#####################")
        print("There are no tags")
        print("#####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
