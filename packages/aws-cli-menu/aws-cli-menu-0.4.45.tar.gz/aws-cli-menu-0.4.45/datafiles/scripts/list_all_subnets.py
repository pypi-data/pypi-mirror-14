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
                print('Getting subnets for vpc for: ' + str(p))
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

                    client2 = session.client('ec2')

                    response = client2.describe_subnets()

                    stacks = response.get('Subnets')

                    subnet_dict = {}
                    for s in stacks:
                        if s['VpcId'] == vpcid:
                            subnet_tag = s.get('Tags')[0]['Value']
                            subnet_cidr_block = s.get('CidrBlock')

                            subnet_dict[
                                'Subnet: ' + str(subnet_cidr_block)] = subnet_tag

                    list.append(p)
                    list.append(name)
                    list.append(vpcid)
                    list.append(cidr_block)
                    list.append(subnet_dict)

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
        print("########################################")
        print('No profiles in .aws/credentials file')
        print("########################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
