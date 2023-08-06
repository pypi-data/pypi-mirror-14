#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    instance_id = raw_input("Enter instance ID to find: [ENTER]")

    info = get_instance_info(session, instance_id)

    print("\n")
    print(pretty(info))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
