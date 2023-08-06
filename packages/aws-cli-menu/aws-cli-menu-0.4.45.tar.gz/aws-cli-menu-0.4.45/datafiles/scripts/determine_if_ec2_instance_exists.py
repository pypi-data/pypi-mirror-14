#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


DEBUG = 0

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)


    instance_name = raw_input('Enter the tag name of the EC2 instance you are searching for: ')

    client = session.client('ec2')
    response = client.describe_instances()

    if (DEBUG):
        print(response)

    stacks = response.get('Reservations')

    menu = {}
    fields = {}
    private_ip = None




    for s in stacks:
        list=[]

        name = None
        id = None

        if 'Tags' in s['Instances'][0]:

            if (DEBUG):
                print('There are tags')

            if len(s.get('Instances')[0]['Tags']) >1:

                if (DEBUG):
                    print('There is more than one tag')

                for t in s.get('Instances')[0]['Tags']:

                    if t['Key'] == 'Name':

                        if instance_name == t['Value']:


                            name = t['Value']

                            if (DEBUG):
                                print('The name tag is: '+str(name))

                                print(s.get('Instances')[0])
                                for k in s.get('Instances')[0]:
                                    print(k+"  "+str(s.get('Instances')[0][k]))


                            if 'PrivateIpAddress' in s.get('Instances')[0]:
                                private_ip=s.get('Instances')[0]['PrivateIpAddress']

                                if (DEBUG):
                                    print('private ip is: '+str(private_ip))

                            id = s.get('Instances')[0]['InstanceId']

                            if (DEBUG):
                                print('instance id is:'+str(id))


            else:
                if (DEBUG):
                    print('There is only one tag')

                if instance_name == s.get('Instances')[0]['Tags'][0]['Value']:
                    name = s.get('Instances')[0]['Tags'][0]['Value'

                    if 'PrivateIpAddress' in s.get('Instances')[0]:
                        private_ip=s.get('Instances')[0]['PrivateIpAddress']
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

            if state == 'running':
                list.append(state)

                if (DEBUG):
                    print('State is running')

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
