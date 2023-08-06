#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpc_peering_connections()
    stacks = response.get('VpcPeeringConnections')

    if len(stacks) > 0:
        dict = {}

        counter = 0
        for s in stacks:
            counter += 1
            print "#######################################"
            print "# Peering Connection #" + str(counter)
            print "#######################################"

            print(pretty(s))
    else:
        print("\n")
        print("###################################")
        print('No vpc peering connections found')
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
