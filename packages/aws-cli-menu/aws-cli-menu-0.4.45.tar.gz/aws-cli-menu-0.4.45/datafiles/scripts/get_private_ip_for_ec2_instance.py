#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)


    instance_name = raw_input('Enter the name of the EC2 instance you are searching for: ')

    client = session.client('ec2')
    response = client.describe_instances()

    if (DEBUG):
        print(response)

    stacks = response.get('Reservations')

    menu = {}
    fields = {}

    name = None


    for s in stacks:
        list=[]


        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:

            if len(s.get('Instances')[0]['Tags']) >1:

                for t in s.get('Instances')[0]['Tags']:
                    if t['Key'] == 'Name':

                        if instance_name == t['Value']:
                            name = t['Value']


            else:
                if instance_name == s.get('Instances')[0]['Tags'][0]['Value']:
                    name = s.get('Instances')[0]['Tags'][0]['Value']
                else:
                    continue
        else:
            continue

        if name:
            list.append(name)
            list.append(id)

            if 'State' in s['Instances'][0]:
                state = s['Instances'][0]['State']['Name']
            else:
                state = 'none'
            list.append(state)

            fields[name] = list


    counter = 0

    if len(fields)>0:


        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item]


        if len(menu) > 0:

            info = get_instance_info(session, menu[1][1])

            print('Private IP Address: '+str(info['PrivateIpAddress']))


        else:
            print("\n\n")
            print('######################')
            print('No instances found')
            print('######################')

    else:
        print("\n\n")
        print('######################')
        print('No instances found')
        print('######################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
