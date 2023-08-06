#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')

    response = client.describe_network_interfaces()

    if 'NetworkInterfaces' in response:
        stacks = response['NetworkInterfaces']

        menu = {}
        counter = 0
        for i in stacks:
            counter += 1
            my_list = []
            my_list.append(i['PrivateIpAddress'])

            if 'Attachment' in i:
                if 'Status' in i['Attachment']:
                    my_list.append(i['Attachment']['Status'])
                    my_list.append(i['Attachment']['InstanceOwnerId'])
                    my_list.append(i['Attachment']['AttachmentId'])
                    menu[counter]= my_list


        if len(menu)>0:
            print "\n\n"
            print '#########################################'
            print '## Select Interface                    ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + str(menu[key][0]) + ' - ' + str(menu[key][1]) + ' - ' + str(menu[key][2])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        attach_id = menu[int(ans)][3]
                        break

            response = client.detach_network_interface(
                DryRun=False,
                AttachmentId=attach_id,
                Force=True
            )

            print("\n")
            print(pretty(response))
        else:
            print("\n")
            print("#################################")
            print("There are no attach interfaces")
            print("#################################")


    else:
        print("\n")
        print("###################################")
        print("No Network Interfaces Available")
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
