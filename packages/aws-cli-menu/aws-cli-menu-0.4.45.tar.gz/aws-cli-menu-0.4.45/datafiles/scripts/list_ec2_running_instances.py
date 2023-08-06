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
    counter=0
    for s in stacks:

        my_list=[]

        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:
            name = s.get('Instances')[0]['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        my_list.append(name)
        my_list.append(id)

        if 'State' in s['Instances'][0]:
            state = s['Instances'][0]['State']['Name']
        else:
            state = 'none'

        if state == 'running'
            counter+=1
            my_list.append(state)

            menu[counter] = my_list


    if len(menu) > 0:

        print("\n")
        print("#########################")
        print("Select Running Instance")
        print("#########################")
        for key in sorted(menu):
            print str(key)+":" + menu[key][0]+'- State: '+str(menu[key][2])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    instance_id = menu[int(ans)][1]
                    break

        info = get_instance_info(session, instance_id)

        print("\n")
        print("##################################")
        print("Instance Information")
        print("##################################")
        print(pretty(info))

    else:
        print("\n\n")
        print('######################')
        print('No instances found')
        print('######################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
