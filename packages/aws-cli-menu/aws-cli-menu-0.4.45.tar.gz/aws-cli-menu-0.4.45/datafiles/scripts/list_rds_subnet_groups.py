#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_subnet_groups()


    if 'DBSubnetGroups' in response:
        stacks = response.get('DBSubnetGroups')

        if len(stacks) > 0:
            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBSupnetGroupName'])
                my_list.append(s)
                menu[counter]=my_list


            print('#######################')
            print('Select Subnet Group')
            print('#######################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Subnet Group Info")
            print("##############################")
            print(pretty(info))

        else:
            print("\n")
            print("########################")
            print('No RDS Subnet Groups')
            print("########################")
    else:
        print("\n")
        print("########################")
        print('No RDS Subnet Groups')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
