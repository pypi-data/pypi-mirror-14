#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_addresses()

    stacks = response.get('Addresses')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for i in stacks:
            counter += 1
            my_list = []

            my_list.append(i['PublicIp'])
            my_list.append(i['Domain'])
            my_list.append(i['AllocationId'])
            menu[counter] = my_list

        print "\n"
        print '#########################################'
        print '## Select Elastic IP Type              ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][0]) + ' - Domain: ' + str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    selected_allocation_id = menu[int(ans)][2]
                    public_ip = menu[int(ans)][0]
                    break

        response = client.release_address(
            DryRun=False,
            # PublicIp=public_ip,
            AllocationId=selected_allocation_id
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("########################")
        print('No elastic IPs found.')
        print("########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
