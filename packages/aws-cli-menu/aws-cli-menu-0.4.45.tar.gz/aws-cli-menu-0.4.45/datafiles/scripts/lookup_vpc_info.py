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

    vpc_id = get_vpc_id()

    session = boto3.session.Session(profile_name=profile_name)
    info = get_info(session, vpc_id)

    print "\n\n"
    print '#########################################'
    print '## VPC Details                         ##'
    print '#########################################'

    print(pretty(info))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
