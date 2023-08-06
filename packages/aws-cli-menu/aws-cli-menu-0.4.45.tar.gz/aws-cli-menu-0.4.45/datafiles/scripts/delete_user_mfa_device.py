#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    menu = get_iam_users(session)

    if len(menu) > 0:

        print("\n")
        print("#################################")
        print("Select User")
        print("#################################")

        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    user_name = menu[int(ans)][0]
                    break

        client = session.client('iam')
        response = client.list_mfa_devices(
            UserName=user_name
            #Marker='string',
            #MaxItems=123
        )


        if 'MFADevices' in response:

            stack = response['MFADevices']
            if len(stack) > 0:
                print("\n")

                menu={}
                counter = 0
                for i in stack:
                    counter+=1
                    my_list = []
                    my_list.append(i['UserName'])
                    my_list.append(i['SerialNumber'])
                    menu[counter]= my_list

                print("\n")
                print("#################################")
                print("Select Device To Deactivate")
                print("#################################")

                for key in sorted(menu):
                    print str(key) + ":" + menu[key][0]+'-'+menu[key][1]

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            serial_number = menu[int(ans)][1]
                            username = menu[int(ans)][0]
                            break

                response = client.delete_virtual_mfa_device(
                    SerialNumber=serial_number
                )

                print("\n")
                print(pretty(response))

            else:
                print("\n")
                print("#############################################")
                print("User does not have any mfa devices.")
                print("#############################################")
        else:
            print("\n")
            print("#############################################")
            print("User does not have any mfa devices.")
            print("#############################################")

    else:
        print("\n")
        print("####################")
        print('No users found')
        print("####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
