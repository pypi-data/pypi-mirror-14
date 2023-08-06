#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_dhcp_options(
        DryRun=False
    )

    if 'DhcpOptions' in response:

        stacks = response['DhcpOptions']

        for i in stacks:
            print("\n")
            print("#######################")
            print("DHCP Options")
            print("#######################")

            print(pretty(i))
    else:
        print("\n")
        print("##########################")
        print("There are no dhcp options")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
