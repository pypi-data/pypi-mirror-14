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
    acls = {}
    acls_to_change = {}
    counter = 0
    assoc_counter = 0

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
                counter += 1

                my_list = []
                my_list.append(s['NetworkAclId'])
                association_count = len(s['Associations'])

                if association_count > 0:
                    my_list.append(association_count)
                    my_list.append(s['Associations'])

                    for i in s['Associations']:
                        assoc_counter += 1
                        acls_to_change[assoc_counter] = i

                else:
                    my_list.append(0)
                    my_list.append([])

                acls[counter] = my_list

        else:
            print("\n")
            print("No network acls.")

    print "\n"
    print '##############################################'
    print '## Select Network ACL Association to Change ##'
    print '##############################################'
    for key in sorted(acls_to_change):
        print str(key) + ": SubnetId:" + str(acls_to_change[key]['SubnetId']) + ' - ACL Id: ' + str(acls_to_change[key]['NetworkAclId'])

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in acls_to_change:
                selected_acl_assoc_id = acls_to_change[
                    int(ans)]['NetworkAclAssociationId']
                selected_acl_id = acls_to_change[int(ans)]['NetworkAclId']
                break

    # Doing this to eliminate the original acl
    new_acls = {}
    new_acl_counter = 0

    for key in acls:

        if selected_acl_id != acls[key][0]:
            new_acl_counter += 1
            new_acls[new_acl_counter] = acls[key]

    print("\n")
    print '##############################################'
    print '## Select new ACL                           ##'
    print '##############################################'
    for key in sorted(new_acls):
        print str(key) + ":" + str(new_acls[key][0])

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in new_acls:
                new_acl_id = new_acls[int(ans)][0]
                break

    client = session.client('ec2')
    response = client.describe_vpcs()

    response = client.replace_network_acl_association(
        DryRun=False,
        AssociationId=selected_acl_assoc_id,
        NetworkAclId=new_acl_id
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
