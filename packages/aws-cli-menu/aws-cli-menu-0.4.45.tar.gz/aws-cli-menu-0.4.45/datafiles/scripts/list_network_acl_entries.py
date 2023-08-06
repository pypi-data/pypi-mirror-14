#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    network_acls = []

    menu = {}
    counter = 0

    for network_acl_iterator in client.network_acls.all():

        acl = {}

        acl_id = network_acl_iterator.id

        client2 = session.client('ec2')
        response = client2.describe_network_acls(
            DryRun=False,
            NetworkAclIds=[acl_id]
        )

        stacks = response.get('NetworkAcls')

        if len(stacks) > 0:
            for s in stacks:
                my_list = []
                counter += 1
                acl_id = s.get('NetworkAclId')
                vpc_id = s.get('VpcId')
                entries = s.get('Entries')
                my_list.append(acl_id)
                my_list.append(vpc_id)
                my_list.append(entries)
                menu[counter] = my_list

        else:
            print("\n")
            print("No network acls.")

    print "\n\n"
    print '#########################################'
    print '## Select Network ACL                  ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_acl_id = menu[int(ans)][0]
                selected_entries = menu[int(ans)][2][0]
                break

    print"\n\n"
    print("###########################")
    print("ACL Entries")
    print("###########################")

    if len(entries) > 0:
        for s in entries:
            print("##########################")
            print("Entry")
            print("##########################")
            print(pretty(s))
    else:
        print("\n")
        print("##########################")
        print("No entries in the acl.")
        print("##########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
