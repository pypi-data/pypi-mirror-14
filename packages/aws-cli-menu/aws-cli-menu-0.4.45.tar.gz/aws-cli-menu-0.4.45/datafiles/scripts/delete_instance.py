#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


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

            # Only interested in instances which are stopped
            if 'state' <> 'terminated':
                continue
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
        print("###################################")
        print("Select Instance To Delete")
        print("###################################")
        print_instance_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        instance_id = menu[int(ans)][1]

        client = session.client('ec2')
        response = client.terminate_instances(
            DryRun=False,
            InstanceIds=[instance_id]
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print('####################################')
        print('No non-terminated instances found')
        print('####################################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
