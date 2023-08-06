#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    use_internal_in_east = yes_or_no('Will you use internal AmazonProvidedDNS in us-east-1 zone?')

    if use_internal_in_east == True:
        domain_name_server = 'AmazonProvidedDNS'
        domain_name = 'ec2.internal'

        DhcpConfig = [
            {'Key':'domain-name','Values':[domain_name]},
            {'Key':'domain-name-servers','Values': [domain_name_server]}
        ]

        response = client.create_dhcp_options(
            DryRun=False,
            DhcpConfigurations=DhcpConfig
        )

        print("\n")
        print(response)

    else:
        using_amazon_dns_in_another_region = yes_or_no("Are you using AmazonProvidedDNS in another region?")


        if using_amazon_dns_in_another_region == True:

            region = select_region()

            domain_name_server = 'AmazonProvidedDNS'
            domain_name = str(region)+'.compute.internal'

            DhcpConfig = [
                {'Key':'domain-name','Values':[domain_name]},
                {'Key':'domain-name-servers','Values': [domain_name_server]}
            ]


            response = client.create_dhcp_options(
                DryRun=False,
                DhcpConfigurations=DhcpConfig
            )

            print("\n")
            print(response)

        else:  # Not using amazon dns


            domain_name_server_ip = raw_input("Enter ip address of domain name server (example 192.168.1.1): [ENTER]")
            domain_name = raw_input("Enter domain name (example: MyCompany.com): [ENTER]")
            #ntp_server = raw_input("Enter ip address of ntp server (example 192.168.1.1): [ENTER]")
            # Add functionality for netbios-name-servers
            # Add functionality for netbios-node-type

            DhcpConfig = [
                {'Key':'domain-name','Values':[domain_name]},
                {'Key':'domain-name-servers','Values': [domain_name_server]}
            ]

            response = client.create_dhcp_options(
                DryRun=False,
                DhcpConfigurations=DhcpConfig
            )

            print("\n")
            print(response)




except (KeyboardInterrupt, SystemExit):
    sys.exit()
