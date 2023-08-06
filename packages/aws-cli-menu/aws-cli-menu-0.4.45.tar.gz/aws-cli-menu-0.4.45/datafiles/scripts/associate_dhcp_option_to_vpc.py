#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_dhcp_options(
        DryRun=False
    )

    if 'DhcpOptions' in response:

        stacks = response['DhcpOptions']

        menu = {}
        counter =0
        for i in stacks:
            counter +=1


            my_list = []
            my_list.append(i['DhcpOptionsId'])
            config = i['DhcpConfigurations']

            for c in config:
                if 'domain-name' in c['Key']:
                    my_list.append(c['Values'][0]['Value'])

            menu[counter]=my_list



        print '#########################################'
        print '## Select DHCP Option to Delege        ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    dhcp_id = menu[int(ans)][0]
                    break




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
            print '############################################'
            print '## Select VPC To Associate To DHCP Option ##'
            print '############################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        vpc_id = menu[int(ans)][1]
                        break


            response = client.associate_dhcp_options(
                DryRun=False,
                DhcpOptionsId=dhcp_id,
                VpcId=vpc_id
            )

            print("\n")
            print(pretty(response))
        else:
            print("\n")
            print("########################################")
            print("No VPCs Available To Associate")
            print("########################################")

    else:
        print("\n")
        print("##########################")
        print("There are no dhcp options")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
