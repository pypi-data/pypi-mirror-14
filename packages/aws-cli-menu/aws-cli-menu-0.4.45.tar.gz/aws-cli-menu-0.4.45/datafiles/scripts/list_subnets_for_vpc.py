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

    for s in stacks:
        list = []

        vpcid = s.get('VpcId')

        if 'Tags' in s:
            name = 'Tag: '+str(s.get('Tags')[0]['Value'])
        else:
            name = 'Tag: None - ' + str(vpcid)

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

        print"\n"

        client = session.client('ec2')

        response = client.describe_subnets()

        if 'Subnets' in response:
            stacks = response.get('Subnets')

            if len(stacks)>0:

                menu={}
                counter = 0
                for s in stacks:

                    if s['VpcId'] == vpc_id:
                        counter += 1
                        my_list = []
                        my_list.append(s['SubnetId'])
                        my_list.append(s)
                        my_list.append(s['CidrBlock'])
                        my_list.append(s['State'])
                        my_list.append(s['DefaultForAz'])
                        menu[counter]=my_list


                if len(menu)>0:
                    print("\n")
                    print("####################################")
                    print("Select Subnet")
                    print("####################################")

                    for key in sorted(menu):
                        print str(key) + ":" + str(menu[key][0])+' - '+str(menu[key][2])+' - '+str(menu[key][3])

                    while True:

                        ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                        if int(ans2) in menu:
                            subnet_id = menu[int(ans2)][0]
                            info = menu[int(ans2)][1]
                            break

                    print("\n")
                    print("###########################")
                    print("Detailed Subnet Info")
                    print("###########################")
                    print(pretty(info))

                else:
                    print("\n")
                    print("#######################")
                    print("No Subnets In This VPC")
                    print("#######################")



            else:
                print("\n")
                print("#######################")
                print("No Subnets In This VPC")
                print("#######################")


        else:
            print("\n")
            print("#######################")
            print("No Subnets In This VPC")
            print("#######################")
    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
