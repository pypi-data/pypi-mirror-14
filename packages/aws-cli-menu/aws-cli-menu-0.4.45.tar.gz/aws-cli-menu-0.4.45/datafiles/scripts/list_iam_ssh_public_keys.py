#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')

    response = client.list_ssh_public_keys()

    if 'SSHPublicKeys' in response:

        stacks = response['SSHPublicKeys']

        if len(stacks) > 0:

                for i in stacks:

                    print("#########################")
                    print("SSH Public Keys")
                    print("#########################")
                    print(pretty(i))
        else:
            print("\n")
            print("##########################")
            print("No SSH Public Keys.")
            print("##########################")

    else:
        print("\n")
        print("##########################")
        print("No SSH Public Keys.")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
