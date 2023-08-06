#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_parameter_groups()


    if 'DBParameterGroups' in response:
        stacks = response.get('DBParameterGroups')

        if len(stacks) > 0:
            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBParameterGroupName'])
                my_list.append(s['DBParameterGroupFamily'])
                my_list.append(s)
                menu[counter]=my_list


            print('#######################')
            print('Select Parameter Group')
            print('#######################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])+' - '+str(menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Parameter Group Info")
            print("##############################")
            print(pretty(info))

        else:
            print("\n")
            print("########################")
            print('No RDS Parameter Groups')
            print("########################")
    else:
        print("\n")
        print("########################")
        print('No RDS Parameter Groups')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
