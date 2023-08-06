#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
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
                    info = menu[int(ans)][2]
                    break

        print("\n")
        print("##################################")
        print("VPN Gateway Info")
        print("##################################")
        print(pretty(info))

    else:
        print("\n")
        print('##############################')
        print('No VPN Gateways')
        print('##############################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
