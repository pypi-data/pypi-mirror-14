#!/usr/bin/env python

"""
List IAM Policies
"""

from __future__ import print_function
import sys
import boto3.session
from aws_cli_menu_helper import pretty
from aws_cli_menu_helper import get_profile_name
import re



try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    CLIENT = SESSION.client('iam')
    RESPONSE = CLIENT.list_policies()

    if 'Policies' in RESPONSE:
        STACKS = RESPONSE.get('Policies')

        if len(STACKS)>0:

            menu = {}
            temp = {}
            for i in STACKS:
                my_list = []
                my_list.append(i['PolicyName'])
                my_list.append(i)
                temp[i['PolicyName']] = my_list

            counter = 0
            for i in sorted(temp):
                counter +=1
                menu[counter]=temp[i]

            print(pretty(menu))
            print("\n")
            print('#######################')
            print('Select Policy')
            print('#######################')
            for key in sorted(menu):
                print(str(key)+" : "+str(menu[key][0]))

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][1]
                        break

            print("\n")
            print("##############################")
            print("Detailed Inline Policy Info")
            print("##############################")
            print(pretty(info))


        else:
            print("\n")
            print("###############################")
            print("There Are No Inline Policies")
            print("###############################")

    else:
        print("\n")
        print("###############################")
        print("There Are No Inline Policies")
        print("###############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
