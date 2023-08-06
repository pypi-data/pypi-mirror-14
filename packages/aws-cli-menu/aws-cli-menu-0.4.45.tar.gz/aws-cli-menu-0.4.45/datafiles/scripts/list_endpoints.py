#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    endpoints = get_endpoints(session)
    stacks = endpoints.get('ServiceNames')

    if len(stacks) > 0:

        for e in stacks:
            print('####################')
            print('Endpoints')
            print('####################')
            print(pretty(e))
    else:
        print("\n")
        print("######################")
        print('No endpoints found')
        print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
