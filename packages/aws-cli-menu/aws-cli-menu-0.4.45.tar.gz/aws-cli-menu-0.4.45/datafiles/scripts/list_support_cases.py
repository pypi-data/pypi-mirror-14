#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('support')

    response = client.describe_cases()

    if 'cases' in response:

        stacks = response['cases']

        for  i in stacks:
            print("############")
            print("Case")
            print("############")

            print(pretty(i))

    else:
        print("\n")
        print("#####################")
        print("There are no cases")
        print("#####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
