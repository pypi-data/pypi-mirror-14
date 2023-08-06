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

            menu = {}
            counter =0
            for s in stacks:
                counter+=1

                my_list = []
                my_list.append(s['NetworkAclId'])
                if len(s['Tags'])>0:
                    my_list.append(s['Tags'])
                else:
                    my_list.append('None')

                my_list.append(s)
                menu[counter]=my_list

                if len(menu)>0:
                    print "\n"
                    print '#############################'
                    print '## Select Network ACL      ##'
                    print '#############################'
                    for key in sorted(menu):
                        print str(key)+": Tags: " + str(menu[key][1]) + ' - '+str(menu[key][0])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                info = menu[int(ans)][2]
                                break

                    print("\n")
                    print(pretty(info))

                else:
                    print("\n")
                    print("######################")
                    print("No network acls.")
                    print("######################")

        else:
            print("\n")
            print("######################")
            print("No network acls.")
            print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
