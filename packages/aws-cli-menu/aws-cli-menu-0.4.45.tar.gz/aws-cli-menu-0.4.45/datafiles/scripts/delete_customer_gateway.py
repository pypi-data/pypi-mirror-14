#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
    response = client.describe_customer_gateways(
        DryRun=False
    )

    if 'CustomerGateways' in response:

        stacks = response['CustomerGateways']

        if (len(stacks) > 0):

            menu = {}
            counter=0
            for ig in stacks:
                counter+=1
                my_list=[]
                my_list.append(ig['CustomerGatewayId'])
                my_list.append(ig['IpAddress'])
                my_list.append(ig['State'])
                my_list.append(ig)
                menu[counter]=my_list

            print "\n"
            print '#########################################'
            print '## Select Customer Gateway'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        id = menu[int(ans)][0]
                        break


            response = client.delete_customer_gateway(
                DryRun=False,
                CustomerGatewayId=id
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##############################")
            print('No customer gateways found')
            print("##############################")

    else:
        print("\n")
        print("##############################")
        print('No customer gateways found')
        print("##############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
