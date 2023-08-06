#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_reserved_instances_offerings(
        DryRun=False
    )


    if 'ReservedInstancesOfferings' in response:
        stacks = response.get('ReservedInstancesOfferings')

        if len(stacks) > 0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['ReservedInstancesOfferingId'])
                my_list.append(s['InstanceType'])
                my_list.append(s)
                menu[counter]=my_list


            print("\n")
            print("####################################")
            print("Select Reserved Instance Offering")
            print("####################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    info = menu[int(ans2)][2]
                    break

            print("\n")
            print("##########################################")
            print("Detailed Reserved Instance Offering Info")
            print("##########################################")

            print("\n")
            print(pretty(info))

        else:
            print("\n")
            print("################################")
            print('No Reserved Instance Offerings')
            print("################################")
    else:
        print("\n")
        print("################################")
        print('No Reserved Instance Offerings')
        print("################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
