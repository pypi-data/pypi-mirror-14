#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')


    print("\n")

    menu= {1:'vpc',2:'standard'}

    print("####################")
    print("Select Domain")
    print("####################")


    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                domain = menu[int(ans)]
                break

    response = client.allocate_address(
        DryRun=False,
        Domain=domain
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
