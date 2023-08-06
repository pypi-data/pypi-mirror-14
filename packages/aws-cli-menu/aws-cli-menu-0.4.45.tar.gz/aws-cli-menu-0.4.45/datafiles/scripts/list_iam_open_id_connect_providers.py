#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')

    response = client.list_open_id_connect_providers()

    if 'OpenIDConnectProviderList' in response:

        stacks = response['OpenIDConnectProviderList']

        if len(stacks) > 0:

                for i in stacks:

                    print("################################")
                    print("Open ID Connect Provider List")
                    print("################################")
                    print(pretty(i))
        else:
            print("\n")
            print("#############################")
            print("No Open ID Connect Providers.")
            print("#############################")

    else:
        print("\n")
        print("##############################")
        print("No Open ID Connect Providers.")
        print("##############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
