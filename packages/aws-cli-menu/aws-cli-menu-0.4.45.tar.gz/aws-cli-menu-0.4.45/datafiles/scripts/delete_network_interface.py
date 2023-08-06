#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import botocore


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

            my_list.append(i['NetworkInterfaceId'])
            my_list.append(i)
            menu[counter] = my_list

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
                        network_id = menu[int(ans)][3]
                        break

            try:
                response = client.delete_network_interface(
                    DryRun=False,
                    NetworkInterfaceId=network_id
                )

                print("\n")
                print(pretty(response))

            except botocore.exceptions.ClientError as e:
                print("\n")
                print(e.message)

                if e.message.endswith('is currently in use.'):
                    print("#######################################")
                    print(" ** Detach Interface First")
                    print("#######################################")

        else:
            print("\n")
            print("##################################")
            print("No Network Interfaces Available")
            print("##################################")
    else:
        print("\n")
        print("###################################")
        print("No Network Interfaces Available")
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
