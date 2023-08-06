#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    print('*** Please wait...this could take a 10 to 15 seconds to collect all the data')
    session = boto3.session.Session(profile_name=profile_name)


    client = session.client('ec2')
    response = client.describe_vpcs()

    if 'Vpcs' in response:
        stacks = response.get('Vpcs')


        if len(stacks)>0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list= []

                if 'Tags' in s:
                    name = 'Tag: '+str(s.get('Tags')[0]['Value'])
                else:
                    name = 'Tag: None - ' + str(vpcid)


                my_list.append(name)
                my_list.append(s['VpcId'])
                my_list.append(s['CidrBlock'])
                menu[counter] = my_list

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

                        subnets = []

                        for s in stacks:
                            if s['VpcId'] == vpc_id:
                                subnets.append(s)

                        menu = {}
                        counter = 0
                        subnet_ids = []
                        for s in subnets:
                            counter+=1
                            my_list = []
                            my_list.append(s['SubnetId'])
                            my_list.append(s['CidrBlock'])
                            subnet_ids.append(s['SubnetId'])
                            my_list.append(s)
                            menu[counter]=my_list


                        if len(subnet_ids)>0:

                            add_all_subnets = yes_or_no('Would You Like To Delete All Subnets')


                            if add_all_subnets == True:

                                for i in subnet_ids:
                                    info = delete_subnet(session, i, False)

                                    print("\n")
                                    print('Deleting subnet: '+str(i))
                                    print(pretty(info))

                            else:

                                print "\n"
                                print '#########################################'
                                print '## Select Subnet To Delete             ##'
                                print '#########################################'
                                for key in sorted(menu):
                                    print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

                                pattern = r'^[0-9]+$'
                                while True:

                                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                                    if re.match(pattern, ans) is not None:
                                        if int(ans) in menu:
                                            info = menu[int(ans)][2]
                                            sn_id = menu[int(ans)][0]
                                            break

                                info = delete_subnet(session, subnet_id, False)

                                print "\n"
                                print '#########################################'
                                print '## Subnet Delete Response              ##'
                                print '#########################################'

                                print(pretty(info))

                        else:
                            print("\n")
                            print("######################")
                            print('No Subnets Found')
                            print("######################")

                    else:
                        print("\n")
                        print("######################")
                        print('No Subnets Found')
                        print("######################")


                else:
                    print("\n")
                    print("######################")
                    print('No Subnets Found')
                    print("######################")


            else:
                print("\n")
                print("######################")
                print('No VPCs Found')
                print("######################")



        else:
            print("\n")
            print("######################")
            print('No VPCs Found')
            print("######################")
    else:
        print("\n")
        print("######################")
        print('No VPCs Found')
        print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
