#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
    response = client.describe_reserved_instances()

    stacks = response.get('ReservedInstances')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]

        id = str(s['ReservedInstanceId'])

        if 'Tags' in s:
            name = s['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        list.append(name)
        list.append(id)


        list.append(s)

        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]


    if len(menu) > 0:

        print("\n")
        print("##########################")
        print("Select Reserved Instance")
        print("##########################")
        for key in sorted(menu):
            print str(key)+":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    info = menu[int(ans)][2]
                    break

        print("\n")
        print("##################################")
        print("Reserved Instance Information")
        print("##################################")
        print(pretty(info))

    else:
        print("\n\n")
        print('##############################')
        print('No reserved instances found')
        print('##############################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
