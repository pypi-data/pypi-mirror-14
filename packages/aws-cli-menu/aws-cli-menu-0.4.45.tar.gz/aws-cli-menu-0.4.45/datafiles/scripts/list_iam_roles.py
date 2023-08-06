#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    menu = get_iam_roles(session)

    if len(menu) > 0:
        print_role_menu(menu)

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")

            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    role_name = menu[int(ans)][0]
                    break

        print"\n"

        s = get_role_info(session, role_name)

        print "\n\n"
        print '#############################'
        print '## Role Info               ##'
        print '#############################'

        print(pretty(s))
    else:
        print "\n\n"
        print '#############################'
        print '## Role Info               ##'
        print '#############################'
        print('No roles found')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
