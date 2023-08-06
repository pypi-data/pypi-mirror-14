#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_security_groups()
    stacks = response.get('SecurityGroups')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for s in stacks:
            counter += 1
            my_list = []
            my_list.append(s['GroupName'])
            if s['GroupName'] == 'ssh-and-http-from-anywhere':
                print('ssh-and-hhtp-from-anywhere security group already exists')
                sys.exit(0)

            my_list.append(s['Description'])
            my_list.append(s)
            menu[counter] = my_list


    def get_info(session, id):
        vpc_client = session.client('ec2')

        response = cf_client.describe_vpcs(VpcIds=[id])
        stacks = response.get('Vpcs')
        return stacks[0]


    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list = []

            if 'Tags' in s:
                name = s.get('Tags')[0]['Value']
            else:
                name = 'None listed - ' + str(s.get('VpcId'))
            vpcid = s.get('VpcId')
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

            print "\n"
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

            print("\n")
            group_name = 'ssh-and-http-from-anywhere'

            description = 'ssh-and-http-from-anywhere'

            response = client.create_security_group(
                DryRun=False,
                GroupName=group_name,
                Description=description,
                VpcId=vpc_id
            )

            group_id = response['GroupId']
            print("\n")
            print(pretty(group_id))

            reponse = client.authorize_security_group_ingress(
                GroupId=str(group_id),
                IpProtocol="tcp",
                CidrIp="0.0.0.0/0",
                FromPort=80,
                ToPort=80
            )

            print("\n")
            print(pretty(response))


            reponse = client.authorize_security_group_ingress(
                GroupId=str(group_id),
                IpProtocol="tcp",
                CidrIp="0.0.0.0/0",
                FromPort=22,
                ToPort=22
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("############################")
            print('No vpc information found')
            print("############################")

    else:
        print("\n")
        print("###########################")
        print('No vpc information found')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
