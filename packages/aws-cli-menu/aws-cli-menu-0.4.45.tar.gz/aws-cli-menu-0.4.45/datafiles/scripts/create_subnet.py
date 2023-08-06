#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    # Get the vpc id

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')


    if 'Vpcs' in response:


        if len(stacks) > 0:


            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []

                if 'Tags' in s:
                    name = 'Tag: '+str(s.get('Tags')[0]['Value'])
                else:
                    name = 'Tag: None - ' + str(s.get('VpcId'))


                my_list.append(name)
                my_list.append(s['VpcId'])
                my_list.append(s['CidrBlock'])
                my_list.append(s)
                menu[counter] = my_list


            if len(menu) > 0:

                print "\n\n"
                print '#########################################'
                print '## Select VPC                          ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key) + ": " + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

                pattern = r'^[0-9]+$'
                while True:

                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            vpc_id = menu[int(ans)][1]
                            vpc_cidr_block = menu[int(ans)][2]
                            vpcid=menu[int(ans)][1]
                            break

                print"\n"


                tenancy_list = ['default', 'dedicated', 'host']
                tenancy = {}

                counter = 0
                for t in sorted(tenancy_list):
                    counter = counter + 1
                    tenancy[counter] = t


                # Get availability zones
                response = client.describe_availability_zones()

                stacks = response.get('AvailabilityZones')

                zones = {}

                if len(stacks) > 0:
                    counter = 0
                    for s in stacks:
                        # print(s)
                        zone_name = s.get('ZoneName')
                        counter = counter + 1
                        zones[counter] = zone_name

                print("\n")
                print("####################################")
                print("Select Availability Zone")
                print("####################################")

                for key in sorted(tenancy):
                    print str(key) + ":" + zones[key]

                while True:

                    ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                    if int(ans2) in zones:
                        zones_ans = zones[int(ans2)]
                        break

                print("\n")

                pattern = r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$'
                while True:

                    cidr = raw_input(
                        "Enter cidr block subordinate to " +
                        str(vpc_cidr_block) +
                        " in the format xxx.xxx.xxx.xxx/xx [ENTER]:")
                    if re.match(pattern, cidr) is not None:
                        cidr_ans = cidr
                        break



                response = client.create_subnet(
                    DryRun=False,
                    VpcId=vpc_id,
                    CidrBlock=cidr_ans,
                    AvailabilityZone=zones_ans
                )

                print("\n")
                print(pretty(response))

        else:
            print("\n")
            print("#######################")
            print ('No vpcs found')
            print("#######################")


    else:
        print("\n")
        print("#######################")
        print ('No vpcs found')
        print("#######################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
