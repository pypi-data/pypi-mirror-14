#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')

    print("\n")
    public_ip = raw_input("Enter public IP address: [ENTER]")
    print("\n")
    bpgasn = raw_input("Enter BGP autonomous systems number(default is 65000): [ENTER]")



    if len(bpgasn) <1:
        bpgasn = 65000
    else:
        bpgasn = int(bpgasn)

    response = client.create_customer_gateway(
        DryRun=False,
        Type='ipsec.1',
        PublicIp=public_ip,
        BgpAsn=bpgasn
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
