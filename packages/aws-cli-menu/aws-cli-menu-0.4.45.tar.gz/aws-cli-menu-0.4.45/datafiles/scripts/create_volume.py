#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    types = [
        ['standard','1-1024'],
        ['gp2','1-16384'],
        ['io1','4-16384']
    ]



    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    # Get availability zones
    response = client.describe_availability_zones()

    stacks = response.get('AvailabilityZones')
    zones = {}

    if len(stacks) > 0:
        counter = 0
        for s in stacks:
            zone_name = s.get('ZoneName')
            counter = counter + 1
            zones[counter] = zone_name

        print("\n")
        print("####################################")
        print("Select Availability Zone")
        print("####################################")

        for key in sorted(zones):
            print str(key) + ":" + zones[key]

        while True:
            ans2 = raw_input("Make a selection: [ENTER](Cntrl-C to exit)")
            if int(ans2) in zones:
                zones_ans = zones[int(ans2)]
                break


        menu = {}
        counter = 0
        for i in sorted(types):
            counter+=1
            my_list = []
            my_list.append(i[0])
            my_list.append(i[1])
            menu[counter]= my_list


        print "\n"
        print '#########################################'
        print '## Select Storage Type                 ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key)+":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern,ans) is not None:
                if int(ans) in menu:
                    size = menu[int(ans)][0]
                    parameters = menu[int(ans)][1]
                    break


        gb = raw_input("Enter size in GB within a range of ("+str(parameters)+"): [ENTER]")
        gb = int(gb)

        client = session.resource('ec2')

        response = client.create_volume(
            VolumeType=size,
            Size=gb,
            AvailabilityZone=zones_ans
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("#######################")
        print("No Availability Zones")
        print("#######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
