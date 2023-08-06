#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('autoscaling')

    print("\n")
    name = raw_input("Enter a name for this launch configuration: [ENTER]")


    client = session.client('ec2')

    response = client.describe_images(
        Filters=[
            {
                'Name': 'owner-id',
                'Values': [
                    '309956199498',
                ]
            },
            {
                'Name': 'image-type',
                'Values': [
                    'machine',
                ]
            },
            {
                'Name': 'architecture',
                'Values': [
                    'x86_64',
                ]
            },
            {
                'Name': 'state',
                'Values': [
                    'available',
                ]
            },
            {
                'Name': 'root-device-type',
                'Values': [
                    'ebs',
                ]
            },
            {
                'Name': 'virtualization-type',
                'Values': [
                    'hvm',
                ]
            },

        ],
    )
    # print(response)

    if 'Images' in response:
        stacks = response.get('Images')
        menu = {}
        counter=0

        for i in stacks:
            counter+=1
            my_list = []
            my_list.append(i['Name'])
            my_list.append(i['ImageId'])
            my_list.append(i)
            menu[counter]=my_list

        if len(menu)>0:
            print "\n"
            print '#########################################'
            print '## Select Image                        ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern,ans) is not None:
                    if int(ans) in menu:
                        image_id = menu[int(ans)][1]
                        break


            client = session.client('ec2')

            response = client.describe_key_pairs()

            if 'KeyPairs' in response:
                stacks = response.get('KeyPairs')

                if len(stacks) > 0:

                    menu = {}
                    counter=0
                    for s in stacks:
                        counter+=1
                        my_list=[]
                        my_list.append(s['KeyName'])
                        my_list.append(s)
                        menu[counter]=my_list

                    print "\n"
                    print '#########################################'
                    print '## Select Key Pair'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key)+":" + menu[key][0]

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern,ans) is not None:
                            if int(ans) in menu:
                                key_name = menu[int(ans)][0]
                                break





                    client = session.client('ec2')
                    response = client.describe_security_groups()
                    stacks = response.get('SecurityGroups')

                    if len(stacks) > 0:

                        menu = {}
                        counter = 0
                        for s in stacks:
                            counter += 1
                            my_list = []
                            my_list.append(s['GroupName'])
                            my_list.append(s['Description'])
                            my_list.append(s)
                            my_list.append(s['GroupId'])
                            menu[counter] = my_list

                        print "\n\n"
                        print '#########################################'
                        print '## Select Security Group               ##'
                        print '#########################################'
                        for key in sorted(menu):
                            print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    sg_id = menu[int(ans)][3]
                                    break


                        types= {
                            'General purpose':[
                                't2.nano',
                                't2.micro',
                                't2.small',
                                't2.medium',
                                't2.large',
                                'm4.large',
                                'm4.xlarge',
                                'm4.2xlarge',
                                'm4.4xlarge',
                                'm4.10xlarge',
                                'm3.medium',
                                'm3.large',
                                'm3.xlarge',
                                'm3.2xlarge'
                            ],
                            'Compute optimized':[
                                'c4.large',
                                'c4.xlarge',
                                'c4.2xlarge',
                                'c4.4xlarge',
                                'c4.8xlarge',
                                'c3.large',
                                'c3.xlarge',
                                'c3.2xlarge',
                                'c3.4xlarge',
                                'c3.8xlarge'
                            ],
                            'Memory optimized':[
                                'r3.large',
                                'r3.xlarge',
                                'r3.2xlarge',
                                'r3.4xlarge',
                                'r3.8xlarge'
                            ],
                            'Storage optimized':[
                                'i2.xlarge',
                                'i2.2xlarge',
                                'i2.4xlarge',
                                'i2.8xlarge',
                                'd2.xlarge',
                                'd2.2xlarge',
                                'd2.4xlarge',
                                'd2.8xlarge'
                            ],
                            'GPU instances':[
                                'g2.2xlarge',
                                'g2.8xlarge'
                            ]


                        }

                        menu = {}
                        counter=0
                        for i in types:
                            counter+=1
                            my_list = []
                            my_list.append(i)
                            my_list.append(types[i])
                            menu[counter]=my_list

                        print "\n"
                        print '#########################################'
                        print '## Select Type Category'
                        print '#########################################'
                        for key in sorted(menu):
                            print str(key) + ":" + menu[key][0]

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    details = menu[int(ans)][1]
                                    break

                        menu = {}
                        counter=0
                        for i in details:
                            counter+=1
                            menu[counter]=i

                        print "\n"
                        print '#########################################'
                        print '## Select Type'
                        print '#########################################'
                        for key in sorted(menu):
                            print str(key) + ":" + menu[key]

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    type = menu[int(ans)]
                                    break


                        print("image id: "+str(image_id))

                        client = session.client('autoscaling')
                        response = client.create_launch_configuration(
                            LaunchConfigurationName=name,
                            ImageId=image_id,
                            KeyName=key_name,
                            SecurityGroups=[ sg_id],

                            #UserData='string',
                            #InstanceId='string',
                            InstanceType=type,
                            #KernelId='string',
                            #RamdiskId='string',
                            #BlockDeviceMappings=[
                            #    {
                            #        'VirtualName': 'string',
                            #        'DeviceName': 'string',
                            #        'Ebs': {
                            #            'SnapshotId': 'string',
                            #            'VolumeSize': 123,
                            #            'VolumeType': 'string',
                            #            'DeleteOnTermination': True|False,
                            #            'Iops': 123,
                            #            'Encrypted': True|False
                            #        },
                            #        'NoDevice': True|False
                            #    },
                            #],
                            InstanceMonitoring={
                                'Enabled': False
                            }
                            #SpotPrice='string',
                            #IamInstanceProfile='string',
                            #EbsOptimized=True|False,
                            #AssociatePublicIpAddress=True|False,
                            #PlacementTenancy='string'
                        )

                        print("\n")
                        print(pretty(response))


        else:
            print("\n")
            print("##############")
            print('No Images')
            print("##############")
    else:
        print("\n")
        print("###############")
        print('No Images')
        print("###############")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
