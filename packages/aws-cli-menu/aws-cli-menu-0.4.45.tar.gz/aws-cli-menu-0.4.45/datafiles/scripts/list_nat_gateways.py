#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_nat_gateways()

    stacks = response.get('NatGateways')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for i in stacks:

            if i['State'] != 'deleted':
                counter += 1
                my_list = []
                my_list.append(i['NatGatewayId'])
                my_list.append(i['SubnetId'])
                my_list.append(i['VpcId'])
                my_list.append(i)
                menu[counter] = my_list

        if len(menu) > 0:
            print "\n"
            print '#########################################'
            print '## Select NAT Gateway                  ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][3]
                        break

            print("\n")
            print("####################################")
            print("Detailed NAT Gateway Information")
            print("####################################")

            print(pretty(info))

        else:
            print("\n")
            print("########################")
            print('No NAT gateways found')
            print("########################")

    else:
        print("\n")
        print("########################")
        print('No NAT gateways found')
        print("########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
