#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profiles = get_all_profiles()

    vpcs = {}

    if len(profiles) > 0:
        for p in profiles:

            try:
                print('Getting vpc: ' + str(p))
                session = boto3.session.Session(profile_name=p)
                client = session.client('ec2')
                response = client.describe_vpcs()
                stacks = response.get('Vpcs')

                vpc_info = {}

                for s in stacks:
                    list = []
                    name = s.get('Tags')[0]['Value']
                    vpcid = s.get('VpcId')
                    cidr_block = s.get('CidrBlock')

                    list.append(p)
                    list.append(name)
                    list.append(vpcid)
                    list.append(cidr_block)

                    vpc_info[cidr_block] = list

                vpcs[p] = vpc_info
            except Exception as e:
                vpcs[p] = 'had a problem'

        for key, value in sorted(vpcs.iteritems()):
            print('######################################')
            print('VPC: ' + str(key))
            print('######################################')

            print(pretty(value))

    else:
        print("\n")
        print("##########################################")
        print('No profiles in .aws/credentials file')
        print("##########################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
