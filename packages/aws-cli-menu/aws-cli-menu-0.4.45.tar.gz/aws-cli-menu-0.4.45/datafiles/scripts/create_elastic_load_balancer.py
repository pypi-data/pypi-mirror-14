#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elb')

    print("\n")

    load_balancer_name = raw_input("Enter name for new load balancer: [ENTER]")

    protocols = ['HTTP', 'HTTPS', 'TCP', 'SS']

    menu = {}
    counter = 0

    for i in sorted(protocols):
        counter += 1
        menu[counter] = i

    print "\n"
    print '#########################################'
    print '## Select Protocol for Front End       ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_frontend_protocol = menu[int(ans)]
                break

    print "\n"
    print '#########################################'
    print '## Select Protocol for Back End       ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_backend_protocol = menu[int(ans)]
                break

    ports = [25, 80, 443, 465, 587]

    menu = {}
    counter = 0

    for i in sorted(ports):
        counter += 1
        menu[counter] = i

    print "\n"
    print '#########################################'
    print '## Select Load Balancer Port           ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + str(menu[key])

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_load_balancer_port = menu[int(ans)]
                break

    print "\n"
    print '###############################################'
    print '## Select Instance Port                      ##'
    print '## Note: Port on which instance is listening ##'
    print '###############################################'
    for key in sorted(menu):
        print str(key) + ":" + str(menu[key])

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_instance_port = menu[int(ans)]
                break

    print("\n")

    client = session.client('iam')
    response = client.list_server_certificates()
    stacks = response['ServerCertificateMetadataList']

    menu = {}
    counter = 0
    if len(stacks) > 0:

        for i in stacks:
            counter += 1
            my_list = []

            my_list.append(i['ServerCertificateId'])
            my_list.append(i['ServerCertificateName'])
            my_list.append(i['Arn'])

            menu[counter] = my_list

        print "\n"
        print '##########################################'
        print '## Select Server Certificate to Utilize ##'
        print '##########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    cert_id = menu[int(ans)][0]
                    arn = menu[int(ans)][2]
                    break
        print"\n"

        client = session.client('ec2')
        response = client.describe_vpcs()
        stacks = response.get('Vpcs')

        menu = {}
        fields = {}

        for s in stacks:
            list = []

            vpcid = s.get('VpcId')

            if 'Tags' in s:
                name = s.get('Tags')[0]['Value']
            else:
                name = 'no tags - ' + str(vpcid)

            cidr_block = s.get('CidrBlock')

            list.append(name)
            list.append(vpcid)
            list.append(cidr_block)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter + 1
            menu[counter] = fields[item]

        if len(menu) > 0:

            print "\n\n"
            print '#########################################'
            print '## Select VPC                          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        vpc_id = menu[int(ans)][1]
                        break

            print"\n\n"

            vpc_id = menu[int(ans)][1]

            response = client.describe_subnets()
            stacks = response.get('Subnets')

            menu = {}
            counter = 0
            for s in stacks:

                if s['VpcId'] == vpc_id:
                    counter += 1
                    my_list = []
                    my_list.append(s['SubnetId'])
                    my_list.append(s['CidrBlock'])

                    menu[counter] = my_list

            print "\n"
            print '#########################################'
            print '## Select Subnet                       ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + str(menu[key][0]) + ' - ' + str(menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        subnet_id = menu[int(ans)][0]
                        break

            client = session.client('elb')
            response = client.create_load_balancer(
                LoadBalancerName=load_balancer_name,
                Listeners=[
                    {
                        'Protocol': selected_frontend_protocol,
                        'LoadBalancerPort': selected_load_balancer_port,
                        'InstanceProtocol': selected_backend_protocol,
                        'InstancePort': selected_instance_port,
                        'SSLCertificateId': arn
                    },
                ],
                # AvailabilityZones=[
                #	avail_zone
                #],
                Subnets=[
                    subnet_id
                ]
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("#####################")
            print("No VPCs available.")
            print("#####################")

    else:
        print("\n")
        print("##########################################################")
        print("There are no certificates.  Create a certificate first.")
        print("##########################################################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
