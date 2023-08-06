#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_dhcp_options(
        DryRun=False
    )

    if 'DhcpOptions' in response:

        stacks = response['DhcpOptions']

        menu = {}
        counter =0
        for i in stacks:
            counter +=1


            my_list = []
            my_list.append(i['DhcpOptionsId'])
            config = i['DhcpConfigurations']

            for c in config:
                if 'domain-name' in c['Key']:
                    my_list.append(c['Values'][0]['Value'])

            menu[counter]=my_list



        print '#########################################'
        print '## Select DHCP Option to Delete        ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    dhcp_id = menu[int(ans)][0]
                    break


        response = client.delete_dhcp_options(
            DryRun=False,
            DhcpOptionsId=dhcp_id
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##########################")
        print("There are no dhcp options")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
