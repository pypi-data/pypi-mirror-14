#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('cloudwatch')

    response = client.describe_alarms()

    if 'MetricAlarms' in response:
        stacks = response.get('MetricAlarms')

        if len(stacks) > 0:

            menu = {}
            counter =0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['Namespace'])
                my_list.append(s['MetricName'])

                if 'AlarmDescription' in s:
                    my_list.append(s['AlarmDescription'])
                else:
                    my_list.append('No Description')
                my_list.append(s)
                menu[counter]=my_list

            print "\n"
            print '#######################'
            print '## Select Alarm      ##'
            print '#######################'
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0]) +' - '+str(menu[key][1])+' - '+str(menu[key][2])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][3]
                        break

            print("\n")
            print("#######################")
            print("Alarm Details")
            print("#######################")
            print(pretty(info))

        else:
            print("\n")
            print("####################")
            print('No MetricAlarms')
            print("####################")
    else:
        print("\n")
        print("###################")
        print('No MetricAlarms')
        print("###################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
