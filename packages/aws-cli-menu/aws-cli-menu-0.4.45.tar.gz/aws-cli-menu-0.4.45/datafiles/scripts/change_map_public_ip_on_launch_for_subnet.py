#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    print('*** Please wait...this could take a 10 to 15 seconds to collect all the data')
    session = boto3.session.Session(profile_name=profile_name)

    menu = get_subnets(session)

    if len(menu) > 0:

        print_subnet_menu(menu)
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        print"\n\n"
        instance_id = menu[int(ans)][1]

        info = get_subnet_info(session, instance_id)
        print "\n\n"
        print '#########################################'
        print '## Current Settings                    ##'
        print '#########################################'

        print('MapPublicIpOnLaunch: ' + str(info[0]['MapPublicIpOnLaunch']))

        id = info[0]['SubnetId']

        menu = {1: ['True', True], 2: ['False', False]}

        print "\n"
        print '#########################################'
        print '## Select                              ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    answer = menu[int(ans)][1]
                    break

        client = session.client('ec2')
        response = client.modify_subnet_attribute(
            SubnetId=id,
            MapPublicIpOnLaunch={
                'Value': answer
            }
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##################")
        print('No subnets found')
        print("##################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
