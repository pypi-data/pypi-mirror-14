#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    for s in stacks:
        list = []

        vpcid = s.get('VpcId')

        if 'Tags' in s:
            name = s.get('Tags')[0]['Value']
        else:
            name = 'no tags - ' + str(vpcid)

        cidr_block = s.get('CidrBlock')

        list.append(name)
        list.append(vpcid)
        list.append(cidr_block)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter + 1
        menu[counter] = fields[item]

    if len(menu) > 0:

        print "\n"
        print '#########################################'
        print '## Select VPC                          ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    vpc_id = menu[int(ans)][1]
                    break

        print"\n\n"



        response = client.describe_subnets()
        stacks = response.get('Subnets')

        menu = {}
        counter = 0
        for s in stacks:

            if s['VpcId'] == vpc_id:
                counter += 1
                my_list = []
                my_list.append(s['SubnetId'])
                my_list.append(s['State'])
                menu[counter] = my_list

        print('######################################')
        print('Select Subnet')
        print('######################################')
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    subnet_id = menu[int(ans)][0]
                    break


        response = client.describe_instances()

        reservations = response.get('Reservations')
        instances = []


        menu = {}
        counter = 0
        for r in reservations:
            #print(pretty(r))
            instances = r['Instances']

            for i in instances:
                counter+=1
                my_list = []
                my_list.append(i['InstanceId'])
                my_list.append(i['InstanceType'])
                my_list.append(i['PrivateIpAddress'])
                menu[counter]=my_list


        if len(menu)>0:
            print("\n")
            print('######################################')
            print('Select Instance To Attach Interface To')
            print('######################################')
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]+'-'+menu[key][2]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        instance_id = menu[int(ans)][0]
                        break

            response = client.describe_network_interfaces()

            if 'NetworkInterfaces' in response:
                stacks = response['NetworkInterfaces']

                # Loop through the interfaces and get the maximum device index
                index = []
                for i in stacks:
                    if 'Attachment' in i:
                        if 'DeviceIndex' in i['Attachment']:
                            index.append(int(i['Attachment']['DeviceIndex']))

                if len(index)>0:
                    device_index = max(index)+1
                else:
                    device_index = 1

                menu = {}
                counter = 0
                for i in stacks:

                    counter += 1
                    my_list = []
                    my_list.append(i['NetworkInterfaceId'])
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
                    menu[counter] = my_list

                if len(menu)>0:
                    print "\n\n"
                    print '#########################################'
                    print '## Select Interface                    ##'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key) + ":" + str(menu[key][1]) + ' - ' + str(menu[key][2]) + ' - ' + str(menu[key][3])

                    pattern = r'^[0-9]+$'
                    while True:

                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                interface_id = menu[int(ans)][0]
                                break

                    response = client.attach_network_interface(
                        DryRun=False,
                        NetworkInterfaceId=interface_id,
                        InstanceId=instance_id,
                        DeviceIndex=device_index
                    )

                    print("\n")
                    print(pretty(response))

                else:
                    print("\n")
                    print("###############################")
                    print("No Network Interfaces")
                    print("###############################")
        else:
            print("\n")
            print("####################################")
            print("No Instances To Attach")
            print("####################################")

    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
