#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')

    response = client.list_instance_profiles()

    if 'InstanceProfiles' in response:

        stacks = response['InstanceProfiles']

        if len(stacks) > 0:

            for i in stacks:
                print("#########################")
                print("Instance Profiles")
                print("#########################")
                print(pretty(i))

        else:
            print("\n")
            print("##########################")
            print("No Instance Profiles.")
            print("##########################")


    else:
        print("\n")
        print("##########################")
        print("No Instance Profiles.")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
