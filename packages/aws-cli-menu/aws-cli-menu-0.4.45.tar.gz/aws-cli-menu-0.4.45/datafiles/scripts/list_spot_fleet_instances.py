#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    response = client.describe_spot_fleet_requests(
        DryRun=False
    )


    if 'SpotFleetRequestConfigs' in response:
        stacks = response.get('SpotFleetRequestConfigs')

        if len(stacks) > 0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['SpotFleetRequestId'])
                my_list.append(s['SpotFleetRequestState'])
                my_list.append(s)
                menu[counter]=my_list


            print("\n")
            print("####################################")
            print("Select Spot Fleet Request")
            print("####################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+menu[key][1]

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in menu:
                    request_id = menu[int(ans2)][0]
                    break


            response = client.describe_spot_fleet_instances(
                DryRun=False,
                SpotFleetRequestId=request_id
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##########################")
            print('No Spot Fleet Request')
            print("#########################")
    else:
        print("\n")
        print("###########################")
        print('No Spot Fleet Request')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
