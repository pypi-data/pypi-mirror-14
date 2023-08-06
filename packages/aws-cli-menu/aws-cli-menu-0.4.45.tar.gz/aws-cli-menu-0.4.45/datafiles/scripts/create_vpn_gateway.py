#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')

    # Get availability zones
    response = client.describe_availability_zones()

    stacks = response.get('AvailabilityZones')

    zones = {}

    if len(stacks) > 0:
        counter = 0
        for s in stacks:
            # print(s)
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

        ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
        if int(ans2) in zones:
            zones_ans = zones[int(ans2)]
            break

    response = client.create_vpn_gateway(
        DryRun=False,
        Type='ipsec.1',
        AvailabilityZone=zones_ans
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
