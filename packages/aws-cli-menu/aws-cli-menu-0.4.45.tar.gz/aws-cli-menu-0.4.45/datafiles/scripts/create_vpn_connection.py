#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

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

                if ig['State'] <> 'deleted':
                    counter+=1
                    my_list=[]
                    my_list.append(ig['CustomerGatewayId'])
                    my_list.append(ig['IpAddress'])
                    my_list.append(ig['State'])
                    my_list.append(ig)
                    menu[counter]=my_list


            if len(menu)>0:
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
                            customer_gateway_id = menu[int(ans)][0]
                            break



                response = client.describe_vpn_gateways(
                    DryRun=False
                )

                stacks = response.get('VpnGateways')

                if len(stacks)>0:

                    menu = {}
                    counter=0
                    for s in stacks:
                        counter+=1
                        my_list=[]

                        my_list.append(s['VpnGatewayId'])
                        my_list.append(s['State'])
                        my_list.append(s)
                        menu[counter]=my_list


                    print("\n")
                    print("##########################")
                    print("Select VPN Gateway")
                    print("##########################")
                    for key in sorted(menu):
                        print str(key)+":" + menu[key][0]+' - '+menu[key][1]

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                vpn_gateway_id = menu[int(ans)][0]
                                break


                    static = yes_or_no('Static Routes Only')

                    response = client.create_vpn_connection(
                        DryRun=False,
                        Type='ipsec.1',
                        CustomerGatewayId=customer_gateway_id,
                        VpnGatewayId=vpn_gateway_id,
                        Options={
                            'StaticRoutesOnly': static
                        }
                    )

                    print("\n")
                    print(pretty(response))

                else:
                    print("\n")
                    print('##############################')
                    print('No VPN Gateways')
                    print('##############################')


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

    else:
        print("\n")
        print("##############################")
        print('No customer gateways found')
        print("##############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
