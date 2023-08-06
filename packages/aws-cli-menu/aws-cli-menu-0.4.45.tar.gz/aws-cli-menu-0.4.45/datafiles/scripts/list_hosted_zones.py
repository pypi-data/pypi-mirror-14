#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    response = list_hosted_zones(session)

    if 'HostedZones' in response:

        stacks = response['HostedZones']

        if len(stacks)>0:

            menu = {}
            counter = 0
            for i in stacks:
                counter+=1
                my_list = []
                my_list.append(i['Name'])
                my_list.append(i)
                menu[counter]=my_list

            print "\n\n"
            print '#########################################'
            print '## Select Hosted Zone                  ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][1]
                        break



            print("\n")
            print("############################")
            print("Hosted Zones Details")
            print("############################")

            print(pretty(info))

        else:
            print("\n")
            print("######################")
            print("No Hosted Zones")
            print("######################")
    else:
        print("\n")
        print("########################")
        print("No Hosted Zones")
        print("########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
