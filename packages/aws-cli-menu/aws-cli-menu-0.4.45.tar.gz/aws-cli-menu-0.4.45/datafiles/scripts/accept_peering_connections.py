#!/usr/bin/env python

"""
Accept a peering connection
"""

from __future__ import print_function
import sys
import boto3.session
from aws_cli_menu_helper import get_profile_name
from aws_cli_menu_helper import pretty
from aws_cli_menu_helper import get_peering_connections
import re

try:
    PROFILE_NAME = get_profile_name()
    print("\n\n")

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)

    PEERING_CONNECTIONS = get_peering_connections(SESSION)

    MENU = {}
    COUNTER = 0

    if len(PEERING_CONNECTIONS)>0:
        for pc in PEERING_CONNECTIONS:
            if 'status_code' in pc:

                if pc['status_code'] == 'pending-acceptance':
                    COUNTER += 1
                    TEMP_LIST = []
                    TEMP_LIST.append(pc['requester_cidr_block'])
                    TEMP_LIST.append(pc['accepter_vpc_id'])
                    TEMP_LIST.append(pc['pc_id'])
                    MENU[COUNTER] = TEMP_LIST

        print("\n")
        print("#####################################")
        print("Select Peering Connection To Accept")
        print("#####################################")
        for key in sorted(MENU):
            print(str(key) + ":" + str(MENU[key][0]) + ' - ' + str(MENU[key][1]))

        PATTERN = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(PATTERN, ans) is not None:
                if int(ans) in MENU:
                    vpc_id = MENU[int(ans)][2]
                    break

        client = SESSION.client('ec2')
        response = client.accept_vpc_peering_connection(
            DryRun=False,
            VpcPeeringConnectionId=vpc_id
        )
        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##########################################")
        print("There are no peering connections to accept")
        print("##########################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
