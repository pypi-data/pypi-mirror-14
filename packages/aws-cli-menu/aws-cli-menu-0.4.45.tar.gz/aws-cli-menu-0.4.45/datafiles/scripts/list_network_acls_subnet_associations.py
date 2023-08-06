#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    network_acls = []

    for network_acl_iterator in client.network_acls.all():

        acl = {}

        acl_id = network_acl_iterator.id

        print("\n")
        print("##################################")
        print('Network ID: ' + str(acl_id))
        print('##################################')

        client2 = session.client('ec2')
        response = client2.describe_network_acls(
            DryRun=False,
            NetworkAclIds=[acl_id]
        )

        stacks = response.get('NetworkAcls')

        if len(stacks) > 0:
            for s in stacks:

                if 'Associations' in s:

                    if len(s['Associations'])>0:
                        print("###############################")
                        print("Network ACL Subnet Association")
                        print("###############################")
                        for i in s['Associations']:
                            print('####################################')
                            print('Subnet: ' + str(i['SubnetId']))
                            print("####################################")
                            print(pretty(i))
                    else:
                        print"######################"
                        print"No Subnet Association"
                        print"######################"
                else:
                    print("\n")
                    print("#########################################")
                    print('No subnet associations for this ACL.')
                    print("#########################################")
        else:
            print("\n")
            print("######################")
            print("No network acls.")
            print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
