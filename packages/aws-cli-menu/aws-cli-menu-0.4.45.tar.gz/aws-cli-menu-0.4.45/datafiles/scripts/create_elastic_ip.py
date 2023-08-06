#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    menu = {1: ['VPC', 'vpc'], 2: ['EC2 Instance', 'standard']}

    print "\n"
    print '#########################################'
    print '## Select Elastic IP Type              ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key][0]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_type = menu[int(ans)][1]
                break

    response = client.allocate_address(
        DryRun=False,
        Domain=selected_type
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
