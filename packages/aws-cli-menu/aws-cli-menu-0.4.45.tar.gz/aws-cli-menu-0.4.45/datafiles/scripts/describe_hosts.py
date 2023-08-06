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
            print("Select Host")
            print("#######################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    info = menu[int(ans2)][2]
                    break

            print("#####################")
            print("Detailed Host Info")
            print("#####################")

            print(pretty(info))


        else:
            print("\n")
            print("#######################")
            print("No Hosts")
            print("#######################")
    else:
        print("\n")
        print("#######################")
        print("No Hosts")
        print("#######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
