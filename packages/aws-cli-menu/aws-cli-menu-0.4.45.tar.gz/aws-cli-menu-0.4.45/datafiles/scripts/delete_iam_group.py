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

    menu = {}
    fields = {}

    for s in stacks:
        list = []
        name = str(s.get('GroupName'))
        id = str(s.get('GroupId'))
        list.append(name)
        list.append(id)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter + 1
        menu[counter] = fields[item]

    print("\n")
    print('#######################')
    print('Groups')
    print('#######################')
    for key in sorted(menu):
        print str(key) + ":" + menu[key][0]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                group_name = menu[int(ans)][0]
                break

    print"\n\n"

    response = client.delete_group(
        GroupName=group_name
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
