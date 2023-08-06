#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    print("\n")
    name = raw_input("Enter name for new security group: [ENTER]")
    print("\n")
    description = raw_input("Enter secrutiy group description: [ENTER]")
    print("\n")
    tag_name = raw_input("Enter tag name: [ENTER]")
    print("\n")
    tag_value = raw_input("Enter tag value: [ENTER]")

    response = client.create_db_security_group(
        DBSecurityGroupName=name,
        DBSecurityGroupDescription=description,
        Tags=[
            {
                'Key': tag_name,
                'Value': tag_value
            },
        ]
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
