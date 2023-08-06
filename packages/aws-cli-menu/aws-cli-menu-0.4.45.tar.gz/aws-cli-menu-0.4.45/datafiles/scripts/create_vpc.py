#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    tenancy_list = ['default', 'dedicated', 'host']
    tenancy = {}

    counter = 0
    for t in sorted(tenancy_list):
        counter = counter + 1
        tenancy[counter] = t


    print("\n")
    print("#########################################################")
    print("NOTE: The supported tenancy options for instances launched")
    print("      into the VPC. A value of default means that instances")
    print("      can be launched with any tenancy; a value of dedicated")
    print("      means all instances launched into the VPC are launched")
    print("      as dedicated tenancy instances regardless of the tenancy")
    print("      assigned to the instance at launch. Dedicated tenancy")
    print("      instances run on single-tenant hardware.")
    print("\n")
    print("Important: The host value cannot be used with this parameter.")
    print("           Use the default or dedicated values only.")
    print("\n")
    print("Select Tenancy.")
    print("##########################################################")


    for key in sorted(tenancy):
        print str(key) + ":" + tenancy[key]

    while True:

        ans2 = raw_input("Enter instance tenancy [ENTER]:")
        if int(ans2) in tenancy:
            tenancy_ans = tenancy[int(ans2)]
            break

    print("\n\n")
    pattern = r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$'
    while True:

        cidr = raw_input(
            "Enter cidr block in format xxx.xxx.xxx.xxx/xx: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, cidr) is not None:
            cidr_ans = cidr
            break


    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.create_vpc(
        DryRun=False,
        CidrBlock=cidr_ans,
        InstanceTenancy=tenancy_ans
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
