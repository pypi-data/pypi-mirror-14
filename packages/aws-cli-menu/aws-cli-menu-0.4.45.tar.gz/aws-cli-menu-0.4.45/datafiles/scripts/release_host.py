#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_hosts()

    if 'Hosts' in response:

        stacks = response['Hosts']
        if len(stacks)>0:

            menu = {}
            counter = 0
            for i in stacks:
                counter+=1
                my_list = []
                my_list.append(i['HostId'])
                my_list.append(i['State'])
                my_list.append(i)
                menu[counter]=my_list

            print("\n")
            print("#######################################")
            print("Select Host To Release")
            print("#######################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    id = menu[int(ans2)][0]
                    break

            response = client.release_hosts(
                HostIds=[id]
            )
            print("\n")
            print(pretty(info))


        else:
            print("\n")
            print("###############################")
            print("No Hosts Available To Release")
            print("###############################")
    else:
        print("\n")
        print("###############################")
        print("No Hosts Available To Release")
        print("###############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
