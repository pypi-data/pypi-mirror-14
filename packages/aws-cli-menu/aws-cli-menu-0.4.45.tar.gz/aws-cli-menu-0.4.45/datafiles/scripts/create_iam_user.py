#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    user_name = raw_input("Enter user name: [ENTER]")

    response = client.create_user(
        UserName=user_name
    )

    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
