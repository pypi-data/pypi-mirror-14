#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    elastic_ips = get_elastic_ips(session)

    menu = {}

    if len(elastic_ips) > 0:

        counter = 0
        for e in elastic_ips:
            counter += 1
            my_list = []

            my_list.append(e['Domain'])
            my_list.append(e['InstanceId'])
            my_list.append(e['NetworkInterfaceId'])
            my_list.append(e['AssociationId'])
            my_list.append(e['NetworkInterfaceOwnerId'])
            my_list.append(e['PublicIp'])
            my_list.append(e['AllocationId'])
            my_list.append(e['PrivateIpAddress'])
            menu[counter] = my_list

        print "\n"
        print '#########################################'
        print '## Select Elastic IP to Disassociate   ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][5]) + ' - ' + str(menu[key][7])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    association_id = menu[int(ans)][3]
                    public_ip = menu[int(ans)][5]
                    break

        client = session.client('ec2')
        response = client.disassociate_address(
            DryRun=False,
            # PublicIp=public_ip,
            AssociationId=association_id
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("############################")
        print('No elastic ips found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
