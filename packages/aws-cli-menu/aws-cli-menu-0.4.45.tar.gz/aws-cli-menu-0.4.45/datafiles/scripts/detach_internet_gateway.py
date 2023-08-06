#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list = []

            if 'Tags' in s:
                name = 'Tags: '+str(s.get('Tags')[0]['Value'])
            else:
                name = 'Tags: None - ' + str(s.get('VpcId'))
            vpcid = s.get('VpcId')
            vpc_cidr_block = s.get('CidrBlock')

            list.append(name)
            list.append(vpcid)
            list.append(vpc_cidr_block)
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

            print"\n"

            vpc_id = menu[int(ans)][1]

            client = session.resource('ec2')

            internet_gateways = []

            for internet_gateways_iterator in client.internet_gateways.all():

                ig = {}
                ig_id = internet_gateways_iterator.id
                ig['ig_id'] = ig_id

                tags = internet_gateways_iterator.tags

                if len(tags) > 0:
                    ig['tags'] = tags
                else:
                    ig['tags'] = ['There are no tags for the vpc']

            internet_gateways.append(ig)

        menu = {}

        counter = 0
        for item in sorted(internet_gateways):
            counter = counter + 1
            my_list = []
            my_list.append(item['ig_id'])
            my_list.append('Tags: '+str(item['tags'][0]))
            menu[counter] = my_list

        if len(menu) > 0:
            print "\n\n"
            print '#########################################'
            print '## Select Internet Gateways            ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + str(menu[key][1])+ ' - '+str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        internet_gateway_id = menu[int(ans)][0]
                        break

            print"\n"

            client = session.client('ec2')
            response = client.detach_internet_gateway(
                DryRun=False,
                InternetGatewayId=internet_gateway_id,
                VpcId=vpc_id
            )
            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##################################")
            print('No Internet Gateways Available')
            print("##################################")

    else:
        print("\n")
        print("###################################")
        print('No Internet Gateways available')
        print("###################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
