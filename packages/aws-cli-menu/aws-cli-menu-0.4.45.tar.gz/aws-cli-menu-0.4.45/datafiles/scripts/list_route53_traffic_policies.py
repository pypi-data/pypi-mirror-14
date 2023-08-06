#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('route53')

    print("\n")
    print("Amazon is throwing error:")
    print("AttributeError: 'Route53' object has no attribute 'list_traffic_policies'")
    print("Will have to wait until amazon gets this fixed.")

    #response = client.list_traffic_policies()

    # print(response)


except (KeyboardInterrupt, SystemExit):
    sys.exit()
