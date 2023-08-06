#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    for s in stacks:
        list = []

        vpcid = s.get('VpcId')

        if 'Tags' in s:
            name = s.get('Tags')[0]['Value']
        else:
            name = 'no tags - ' + str(vpcid)

        cidr_block = s.get('CidrBlock')

        list.append(name)
        list.append(vpcid)
        list.append(cidr_block)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter + 1
        menu[counter] = fields[item]

    if len(menu) > 0:

        print "\n"
        print '#########################################'
        print '## Select VPC                          ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    vpc_id = menu[int(ans)][1]
                    break

        response = client.create_route_table(
            DryRun=False,
            VpcId=vpc_id
        )

        print("\n")
        print("############################")
        print("New Route Table Information")
        print("############################")
        print(pretty(response))


    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
