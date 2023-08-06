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
                else:
                    my_list.append('not defined')
                    my_list.append('not defined')
            else:
                my_list.append('not defined')
                my_list.append('not defined')

            my_list.append(i)

            if 'TagSet' in i:
                if len(i['TagSet'])>0:
                    my_list.append(i['TagSet'])
                else:
                    my_list.append('None')

            menu[counter] = my_list

        if len(menu)>0:
            print "\n\n"
            print '#########################################'
            print '## Select Interface                    ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ": Tags: " + str(menu[key][4])+' - '+str(menu[key][0]) + ' - ' + str(menu[key][1]) + ' - ' + str(menu[key][2])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        details = menu[int(ans)][3]
                        break

            print("\n")
            print("################################")
            print("Interface Details")
            print("################################")
            print(pretty(details))

        else:
            print("\n")
            print("#################################")
            print("No Network Interfaces Available")
            print("#################################")
    else:
        print("\n")
        print("###################################")
        print("No Network Interfaces Available")
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
