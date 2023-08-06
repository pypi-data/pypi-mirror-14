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

            print("\n")
            print("######################################")
            print("Virtual MFA Devices")
            print("######################################")

            for i in stacks:
                print("################")
                print("Device")
                print("################")
                print(pretty(i))
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
