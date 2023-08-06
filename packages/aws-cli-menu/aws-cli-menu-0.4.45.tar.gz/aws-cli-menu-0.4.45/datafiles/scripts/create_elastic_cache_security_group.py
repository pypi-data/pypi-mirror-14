#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')

    print("\n")
    name = raw_input("Enter new security group name: [ENTER]")
    print("\n")
    description = raw_input("Enter security group description: [ENTER]")

    response = client.create_cache_security_group(
        CacheSecurityGroupName=name,
        Description=description
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
