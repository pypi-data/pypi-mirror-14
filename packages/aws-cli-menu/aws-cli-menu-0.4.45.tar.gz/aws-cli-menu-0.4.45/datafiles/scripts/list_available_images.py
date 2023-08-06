#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
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
                        info = menu[int(ans)][2]
                        break

            print("\n")
            print("###############################")
            print("Detailed Image Information")
            print("###############################")
            print(pretty(info))

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
