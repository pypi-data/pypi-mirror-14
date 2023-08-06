#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_reserved_instances_modifications()


    if 'ReservedInstancesModifications' in response:
        stacks = response.get('ReservedInstancesModifications')

        if len(stacks) > 0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['ReservedInstancesModificationId'])
                my_list.append(s['Status'])
                my_list.append(s)
                menu[counter]=my_list


            print("\n")
            print("#######################################")
            print("Select Reserved Instance Modification")
            print("#######################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    info = menu[int(ans2)][2]
                    break

            print("\n")
            print("#############################################")
            print("Detailed Reserved Instance Modification Info")
            print("#############################################")

            print("\n")
            print(pretty(info))

        else:
            print("\n")
            print("###################################")
            print('No Reserved Instance Modifications')
            print("###################################")
    else:
        print("\n")
        print("###################################")
        print('No Reserved Instance Modifications')
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
