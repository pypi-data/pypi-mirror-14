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
                my_list.append(acl_id)
                my_list.append(vpc_id)
                my_list.append(s['IsDefault'])
                menu[counter] = my_list

        else:
            print("\n")
            print("No network acls.")

    print "\n\n"
    print '#########################################'
    print '## Network ACLs                        ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_acl_id = menu[int(ans)][0]
                is_default = menu[int(ans)][2]
                break

    if is_default == True:
        print("\n")
        print("############################")
        print("Can not delete default ACL")
        print("############################")

    else:
        print"\n"
        client = session.client('ec2')
        response = client.delete_network_acl(
            DryRun=False,
            NetworkAclId=selected_acl_id
        )

        print("\n")
        print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
