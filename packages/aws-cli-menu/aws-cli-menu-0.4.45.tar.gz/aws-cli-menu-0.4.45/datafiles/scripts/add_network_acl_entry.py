#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import re


try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    network_acls = []

    menu = {}
    rules = {}

    ports = {
        22: {'name': 'SSH', 'protocol': 'tcp', 'port': 22, 'protocol_number': 6},
        23: {'name': 'telnet', 'protocol': 'tcp', 'port': 23, 'protocol_number': 6},
        25: {'name': 'SMTP', 'protocol': 'tcp', 'port': 25, 'protocol_number': 6},
        42: {'name': 'nameserver', 'protocol': 'tcp', 'port': 42, 'protocol_number': 6},
        53: {'name': 'DNS', 'protocol': 'udp', 'port': 53, 'protocol_number': 6},
        53: {'name': 'DNS', 'protocol': 'tcp', 'port': 53, 'protocol_number': 6},
        80: {'name': 'HTTP', 'protocol': 'tcp', 'port': 80, 'protocol_number': 6},
        110: {'name': 'POP3', 'protocol': 'tcp', 'port': 110, 'protocol_number': 6},
        143: {'name': 'IMAP', 'protocol': 'tcp', 'port': 143, 'protocol_number': 6},
        389: {'name': 'LDAP', 'protocol': 'tcp', 'port': 389, 'protocol_number': 6},
        443: {'name': 'HTTPS', 'protocol': 'tcp', 'port': 443, 'protocol_number': 6},
        465: {'name': 'SMTPS', 'protocol': 'tcp', 'port': 465, 'protocol_number': 6},
        993: {'name': 'IMAPS', 'protocol': 'tcp', 'port': 993, 'protocol_number': 6},
        995: {'name': 'POP3S', 'protocol': 'tcp', 'port': 995, 'protocol_number': 6},
        1433: {'name': 'MS SQL', 'protocol': 'tcp', 'port': 1433, 'protocol_number': 6},
        1521: {'name': 'Oracle', 'protocol': 'tcp', 'port': 1521, 'protocol_number': 6},
        3306: {'name': 'MySQL/Aurora', 'protocol': 'tcp', 'port': 3306, 'protocol_number': 6},
        3389: {'name': 'RDP', 'protocol': 'tcp', 'port': 3389, 'protocol_number': 6},
        5432: {'name': 'PostgresSQL', 'protocol': 'tcp', 'port': 5432, 'protocol_number': 6},
        5439: {'name': 'Redshift', 'protocol': 'tcp', 'port': 5439, 'protocol_number': 6},
        8080: {'name': 'HTTP*', 'protocol': 'tcp', 'port': 8080, 'protocol_number': 6},
        8443: {'name': 'HTTPS*', 'protocol': 'tcp', 'port': 8443, 'protocol_number': 6},
    }

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
            print("####################")
            print("No network acls.")
            print("####################")

    # Before we continue, get the cidr block for the vpc
    client = session.client('ec2')
    response = client.describe_vpcs(VpcIds=[vpc_id])

    stacks = response.get('Vpcs')
    vpc_cidr_block = stacks[0]['CidrBlock']

    print "\n"
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
                selected_entries = menu[int(ans)][2]
                break

    if len(selected_entries) > 0:

        for e in selected_entries:

            rules[e.get('RuleNumber')] = 1

        rules_menu = {}

        counter =0
        for i in sorted(ports):
            counter+=1
            my_list= []
            my_list.append(i)
            my_list.append(ports[i])
            rules_menu[counter]=my_list



        print "\n"
        print '#########################################'
        print '## Select Rule to Add                  ##'
        print '#########################################'

        for key in sorted(rules_menu):
            print str(key) + ": Port: "+str(rules_menu[key][0]) +' - '+ str(rules_menu[key][1]['name'])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in rules_menu:
                    print(pretty(rules_menu[int(ans)][1]))
                    selected_rule = rules_menu[int(ans)][1]
                    break


        pattern = r'^[0-9]+$'
        print("\n")
        while True:
            rule_number = raw_input("Enter an abitrary rule number: [ENTER]")
            if re.match(pattern, rule_number) is not None:

                if rule_number not in rules_menu:
                    selected_rule_number = rule_number
                    break
                else:
                    print(
                        'Rule number already utilized, select a different rule number.')

        print("rule number is: " + str(selected_rule_number))

        rule_direction = {1: ['Inbound', False], 2: ['Outbound', True]}

        print "\n"
        print '#########################################'
        print '## Select Inbound or Outbound Rule     ##'
        print '#########################################'
        for key in sorted(rule_direction):
            print str(key) + ":" + rule_direction[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in rule_direction:
                    egress_selection = rule_direction[int(ans)][1]
                    break

        print('egress selection: ' + str(egress_selection))

        authorization = {1: ['Allow', 'allow'], 2: ['Deny', 'deny']}
        print "\n"
        print '#############################################'
        print '## Select whether to allow or deny traffic ##'
        print '#############################################'
        for key in sorted(authorization):
            print str(key) + ":" + authorization[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in authorization:
                    authorization_selection = authorization[int(ans)][1]
                    break

        pattern = r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$'
        print("\n")
        while True:
            cidr_block = raw_input(
                "Enter the cidr block in the format (" +
                str(vpc_cidr_block) +
                "): [ENTER](Cntrl-C to exit)")
            if re.match(pattern, cidr_block) is not None:

                selected_cidr_block = cidr_block
                break
            else:
                print('Incorrect format.')


        protocol = selected_rule['protocol_number']
        cidr_block = selected_cidr_block
        port = selected_rule['port']



        client = session.client('ec2')

        response = client.create_network_acl_entry(
            DryRun=False,
            NetworkAclId=selected_acl_id,
            RuleNumber=int(rule_number),
            Protocol=str(protocol),
            RuleAction=authorization_selection,
            Egress=egress_selection,
            CidrBlock=cidr_block,
            PortRange={
                'From': int(port),
                'To': int(port)
            }
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("#############################")
        print("There are no ACL entries.")
        print("#############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
