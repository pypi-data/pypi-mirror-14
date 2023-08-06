#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    ar = session.get_available_resources()

    if len(ar) > 0:
        print("\n\n")
        for item in sorted(ar):
            print (item)
    else:
        print("\n")
        print("######################")
        print('No resources found')
        print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
