#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')
    menu = get_iam_roles(session)

    if len(menu) > 0:
        print_role_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        role_name = menu[int(ans)][0]

        print"\n\n"

        response = client.delete_role(
            RoleName=role_name
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("#################################")
        print('No Roles available to delete.')
        print("#################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
