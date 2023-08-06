#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    def get_info(session, id):
        vpc_client = session.client('ec2')

        response = cf_client.describe_vpcs(VpcIds=[id])
        stacks = response.get('Vpcs')
        return stacks[0]

    session = boto3.session.Session(profile_name=profile_name)
    cf_client = session.client('ec2')
    response = cf_client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list = []

            if 'Tags' in s:
                name = s.get('Tags')[0]['Value']
            else:
                name = 'None listed - ' + str(s.get('VpcId'))
            vpcid = s.get('VpcId')
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

            print "\n\n"
            print '#########################################'
            print '## VPCs                                ##'
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

            print"\n"

            vpc_id = menu[int(ans)][1]

            response = cf_client.create_network_acl(
                DryRun=False,
                VpcId=vpc_id
            )

        else:
            print("\n")
            print("############################")
            print('No vpc information found')
            print("############################")

    else:
        print("\n")
        print("###########################")
        print('No vpc information found')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
