#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    session = boto3.session.Session(profile_name=PROFILE_NAME)
    client = session.client('ecs')


    response = client.list_task_definition_families()

    print("\n")
    #print(pretty(response))

    families = response.get('families')

    menu = {}
    fields = {}

    for s in families:

        list = []

        list.append(s)
        fields[s] = list

    counter = 0
    for item in sorted(fields):
        counter = counter + 1
        menu[counter] = fields[item]

    if len(menu) > 0:

        print "\n"
        print '#########################################'
        print '## Families                            ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    name = menu[int(ans)][0]
                    break

        print"\n"

except (KeyboardInterrupt, SystemExit):
    sys.exit()
