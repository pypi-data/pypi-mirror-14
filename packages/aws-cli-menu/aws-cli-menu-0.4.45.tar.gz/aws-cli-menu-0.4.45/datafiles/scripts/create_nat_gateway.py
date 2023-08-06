#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    print('*** Please wait...this could take a 10 to 15 seconds to collect all the data')
    session = boto3.session.Session(profile_name=profile_name)

    menu = get_subnets(session)

    if len(menu) > 0:

        print_subnet_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        subnet_id = menu[int(ans)][1]

        info = get_subnet_info(session, subnet_id)

        vpc_id = info[0]['VpcId']

        elastic_ips = get_elastic_ips(session)

        if len(elastic_ips) > 0:

            menu = {}
            counter = 0
            for i in elastic_ips:
                counter += 1
                my_list = []
                my_list.append(i['PublicIp'])
                my_list.append(i['Domain'])
                my_list.append(i['AllocationId'])
                menu[counter] = my_list

            print "\n\n"
            print '#########################################'
            print '## Select Elastic IP                   ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        allocation_id = menu[int(ans)][2]
                        break

            token = raw_input(
                "Enter Client Token (case-sensitive identifier you provide to ensure the idempotency of the request): [ENTER]")

            client = session.client('ec2')
            response = client.create_nat_gateway(
                SubnetId=subnet_id,
                AllocationId=allocation_id,
                ClientToken=token
            )

            print(pretty(response))

        else:
            print("\n")
            print("####################################################################")
            print("There are no elastic IPs.  You need to create an elastic IP first.")
            print("####################################################################")


    else:
        print("\n")
        print("#####################")
        print('No subnets found')
        print("#####################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
