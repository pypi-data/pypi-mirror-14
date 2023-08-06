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


                        add_all_subnets = yes_or_no('Would You Like To Add All Subnets')


                        if add_all_subnets == True:

                            print("\n")
                            subnet_group_name = raw_input("Enter subnet group name: [ENTER] ")

                            print("\n")
                            subnet_group_description = raw_input("Enter subnet group description: [ENTER] ")

                            print("\n")
                            tag_name = raw_input("Enter tag name: [ENTER] ")

                            print("\n")
                            tag_value = raw_input("Enter tag value: [ENTER] ")

                            subids_to_add = str1 = '","'.join(subnet_ids)
                            subids_to_add = '"'+subids_to_add+'"'

                            client = session.client('rds')
                            response = client.create_db_subnet_group(
                                DBSubnetGroupName=subnet_group_name,
                                DBSubnetGroupDescription=subnet_group_description,
                                SubnetIds=[subids_to_add],
                                Tags=[
                                    {
                                        'Key': tag_name,
                                        'Value': tag_value
                                    }
                                ]
                            )

                        else:
                            print "\n"
                            print '#########################################'
                            print '## Select Subnet                       ##'
                            print '#########################################'
                            for key in sorted(menu):
                                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1]

                            pattern = r'^[0-9]+$'
                            while True:

                                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                                if re.match(pattern, ans) is not None:
                                    if int(ans) in menu:
                                        info = menu[int(ans)][2]
                                        break


                            print("\n")
                            subnet_group_name = raw_input("Enter subnet group name: [ENTER] ")

                            print("\n")
                            subnet_group_description = raw_input("Enter subnet group description: [ENTER] ")

                            print("\n")
                            tag_name = raw_input("Enter tag name: [ENTER] ")

                            print("\n")
                            tag_value = raw_input("Enter tag value: [ENTER] ")

                            client = session.client('rds')
                            response = client.create_db_subnet_group(
                                DBSubnetGroupName=subnet_group_name,
                                DBSubnetGroupDescription=subnet_group_description,
                                SubnetIds=[info['SubnetId']],
                                Tags=[
                                    {
                                        'Key': tag_name,
                                        'Value': tag_value
                                    }
                                ]
                            )

                            print("\n")
                            print(pretty(response))


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

        else:
            print("\n")
            print("############################")
            print('No vpc information found')
            print("############################")


    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
