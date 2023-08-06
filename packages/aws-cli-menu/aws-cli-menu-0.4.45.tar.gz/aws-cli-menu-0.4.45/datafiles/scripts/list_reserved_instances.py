#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_reserved_instances(
        DryRun=False
    )


    if 'ReservedInstances' in response:
        stacks = response.get('ReservedInstances')

        if len(stacks) > 0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['ReservedInstancesId'])
                my_list.append(s['InstanceType'])
                my_list.append(s)
                menu[counter]=my_list


            print("\n")
            print("####################################")
            print("Select Reserved Instance")
            print("####################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    info = menu[int(ans2)][2]
                    break

            print("\n")
            print("################################")
            print("Detailed Reserved Instance Info")
            print("################################")

            print("\n")
            print(pretty(info))

        else:
            print("\n")
            print("##########################")
            print('No Reserved Instances')
            print("#########################")
    else:
        print("\n")
        print("###########################")
        print('No Reserved Instances')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
