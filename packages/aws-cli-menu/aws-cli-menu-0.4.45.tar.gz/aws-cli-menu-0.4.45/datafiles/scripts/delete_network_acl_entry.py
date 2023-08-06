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

    pattern = r'^[iIoO]$'
    while True:
        ans = raw_input("Select inbound or outbound entries (I or O).")
        if re.match(pattern, ans) is not None:

            if ans == 'i' or ans == "I":
                egress = False
                break
            else:
                egress = True
                break

    print"\n"

    if len(entries) > 0:
        counter = 0
        entry_menu = {}
        for s in entries:

            if s['Egress'] == egress:
                counter += 1
                my_list = []
                my_list.append(s['CidrBlock'])
                my_list.append(s['RuleNumber'])
                my_list.append(s['Protocol'])
                my_list.append(s['Egress'])
                my_list.append(s['RuleAction'])
                if 'PortRange' in s:
                    my_list.append(s['PortRange']['To'])
                else:
                    my_list.append('All')

                entry_menu[counter] = my_list

        print "\n\n"
        print '#############################################'
        print '## Select acl entry to delete ##'
        print '#############################################'
        for key in sorted(entry_menu):
            print str(key) + ":" + str(entry_menu[key][0]) + ' - protocol: ' + str(entry_menu[key][2]) + ' - actions: ' + str(entry_menu[key][4]) + ' - port: ' + str(entry_menu[key][5])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in entry_menu:
                    entry_selection = entry_menu[int(ans)]
                    break

        client = session.client('ec2')
        response = client.delete_network_acl_entry(
            DryRun=False,
            NetworkAclId=selected_acl_id,
            RuleNumber=entry_selection[1],
            Egress=egress
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("#########################")
        print("No entries in the acl.")
        print("#########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
