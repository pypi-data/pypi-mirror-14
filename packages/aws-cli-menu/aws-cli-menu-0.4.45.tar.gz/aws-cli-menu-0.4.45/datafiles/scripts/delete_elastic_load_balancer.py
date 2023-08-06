#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('elb')

    response = client.describe_load_balancers()

    if 'LoadBalancerDescriptions' in response:
        stacks = response.get('LoadBalancerDescriptions')

        if len(stacks) > 0:

            menu = {}
            counter = 0
            for s in stacks:
                counter += 1
                menu[counter] = s.get('LoadBalancerName')

            print "\n"
            print '#########################################'
            print '## Select Load Balancer to Delete      ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        elb_name = menu[int(ans)]
                        break

            response = client.delete_load_balancer(
                LoadBalancerName=elb_name
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("#####################")
            print('No Load Balancers')
            print("#####################")
    else:
        print("\n")
        print("#####################")
        print('No Load Balancers')
        print("#####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
