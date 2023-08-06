#!/usr/bin/env python

import boto3.session
import sys
from aws_cli_menu_helper import *


from aws_cli_menu_helper import *


try:
    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    peering_connections = get_peering_connections(session)

    menu = {}
    counter = 0

    for pc in peering_connections:
        if 'status_code' in pc:

            if pc['status_code'] == 'active':
                counter += 1
                temp_list = []

                temp_list.append(pc['requester_cidr_block'])
                temp_list.append(pc['accepter_vpc_id'])
                temp_list.append(pc['pc_id'])
                menu[counter] = temp_list

    print("\n")
    print("##########################")
    print("Select Peering Connection")
    print("##########################")

    for key in sorted(menu):
        print(str(key) + ":" + str(menu[key][0]) + ' - ' + str(menu[key][1]))

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                vpc_id = menu[int(ans)][2]
                break

    client = session.client('ec2')

    response = client.delete_vpc_peering_connection(
        DryRun=False,
        VpcPeeringConnectionId=vpc_id
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
