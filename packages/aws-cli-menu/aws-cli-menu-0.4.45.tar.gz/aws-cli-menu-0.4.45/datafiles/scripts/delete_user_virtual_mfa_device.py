#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)


    client = session.client('iam')
    response = client.list_virtual_mfa_devices(
        AssignmentStatus='Any'
        #Marker='string',
        #MaxItems=123
    )

    if 'VirtualMFADevices' in response:

        stacks = response['VirtualMFADevices']
        if len(stacks)>0:

            menu= {}
            counter = 0
            for i in stacks:
                counter+=1
                menu[counter]=i['SerialNumber']

            print("#################################")
            print("Select Device To Delete")
            print("#################################")

            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        ser_num = menu[int(ans)]
                        break


            response = client.delete_virtual_mfa_device(
                SerialNumber=ser_num
            )
            print("\n")
            print(pretty(response))



        else:
            print("\n")
            print("####################################")
            print("There are no virtual mfa devices")
            print("####################################")

    else:
        print("\n")
        print("####################################")
        print("There are no virtual mfa devices")
        print("####################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
