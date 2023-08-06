#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    print('*** Please wait...this could take a 10 to 15 seconds to collect all the data')
    session = boto3.session.Session(profile_name=profile_name)

    menu = get_subnets(session)

    if len(menu) > 0:

        print_subnet_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        instance_id = menu[int(ans)][1]

        info = get_subnet_info(session, instance_id)

        print "\n\n"
        print '#########################################'
        print '## Subnet Info                         ##'
        print '#########################################'

        print(pretty(info))
    else:
        print("\n")
        print("#####################")
        print('No subnets found')
        print("#####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
