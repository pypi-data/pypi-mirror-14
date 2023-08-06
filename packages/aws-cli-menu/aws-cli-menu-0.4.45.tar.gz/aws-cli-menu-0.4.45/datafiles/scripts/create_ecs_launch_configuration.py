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
    name = 'ecs-launch-configuration'


    client = session.client('ec2')

    response = client.describe_images(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [
                    'ami-67a3a90d',
                ]
            }
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
                                't2.micro'
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

                            UserData="#!/bin/bash\necho ECS_CLUSTER=my-ecs-cluster > /etc/ecs/ecs.config",
                            #InstanceId='string',
                            InstanceType=type,
                            #KernelId='string',
                            #RamdiskId='string',

                            BlockDeviceMappings = [
                                {
                                    'DeviceName': '/dev/xvdb',
                                    'Ebs': {
                                        #'SnapshotId':'snap-516c7c43',
                                        'VolumeSize': 8,
                                        'DeleteOnTermination': True,
                                        'Encrypted':False,
                                        'VolumeType':'standard',
                                        'Iops':300
                                    }
                                },
                                {
                                    'DeviceName': '/dev/xvdcz',
                                    'Ebs': {
                                        'VolumeSize': 22,
                                        'DeleteOnTermination': True,
                                        'Encrypted':False,
                                        'VolumeType':'standard',
                                        'Iops':900
                                    }
                                }
                            ],
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
                            },
                            #SpotPrice='string',
                            IamInstanceProfile='ecs-instance-role',
                            #EbsOptimized=True|False,
                            AssociatePublicIpAddress=True
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
