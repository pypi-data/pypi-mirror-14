#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
    response = client.describe_instances()

    if (DEBUG):
        print(response)

    stacks = response.get('Reservations')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]

        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:
            name = s.get('Instances')[0]['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        list.append(name)
        list.append(id)

        if 'State' in s['Instances'][0]:
            state = s['Instances'][0]['State']['Name']
        else:
            state = 'none'
        list.append(state)

        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]


    if len(menu) > 0:

        print("\n")
        print("######################")
        print("Select Instance")
        print("######################")
        for key in sorted(menu):
            print str(key)+":" + menu[key][0]+'- State: '+str(menu[key][2])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    instance_id = menu[int(ans)][1]
                    break

        attribute = [
            'instanceType',
            'kernel',
            'ramdisk',
            'userData',
            'disableApiTermination',
            'instanceInitiatedShutdownBehavior',
            'rootDeviceName',
            'blockDeviceMapping',
            'productCodes',
            'sourceDestCheck',
            'groupSet',
            'ebsOptimized',
            'sriovNetSupport'
        ]

        menu = {}
        counter = 0
        for i in sorted(attribute):
            counter+=1
            menu[counter]=i


        print("\n")
        print("######################")
        print("Select Attribute To Reset")
        print("######################")
        for key in sorted(menu):
            print str(key)+":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    attribute_name = menu[int(ans)]
                    break


        response = client.reset_instance_attribute(
            DryRun=False,
            InstanceId=instance_id,
            Attribute=attribute_name
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n\n")
        print('######################')
        print('No instances found')
        print('######################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
