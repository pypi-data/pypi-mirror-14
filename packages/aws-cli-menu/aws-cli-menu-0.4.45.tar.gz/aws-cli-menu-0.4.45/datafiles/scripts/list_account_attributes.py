#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_account_attributes()

    if 'AccountAttributes' in response:
        stacks = response.get('AccountAttributes')

        if len(stacks) > 0:

            for s in stacks:
                print('#####################')
                print('Account Attribute')
                print('#####################')
                print(pretty(s))

        else:
            print("\n")
            print("##########################")
            print('No Account Attributes')
            print("##########################")
    else:
        print("\n")
        print("##########################")
        print('No Account Attributes')
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
