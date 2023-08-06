#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('autoscaling')


    response = client.describe_launch_configurations()

    stacks = response.get('LaunchConfigurations')


    if len(stacks)>0:

        menu = {}
        counter = 0

        for s in stacks:
            counter+=1
            my_list=[]
            my_list.append(s['LaunchConfigurationName'])
            my_list.append(s)
            menu[counter]=my_list


        print "\n\n"
        print '###############################'
        print '## Select Launch Configuration'
        print '###############################'
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    info = menu[int(ans)][1]
                    break


        print("\n")
        print("###################################")
        print("Detailed Launch Configuration Info")
        print("###################################")
        print(pretty(info))


    else:
        print("\n")
        print("################################")
        print('No launch configurations found')
        print("################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
