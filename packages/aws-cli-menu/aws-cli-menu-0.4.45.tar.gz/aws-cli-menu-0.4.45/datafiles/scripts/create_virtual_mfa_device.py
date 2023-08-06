#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    print"\n"
    device_name = raw_input("Enter virtual device name name: [ENTER]")

    response = client.create_virtual_mfa_device(
        VirtualMFADeviceName=device_name
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
