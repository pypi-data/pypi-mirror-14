#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_security_groups()


    if 'DBSecurityGroups' in response:
        stacks = response.get('DBSecurityGroups')

        if len(stacks) > 0:
            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBSecurityGroupName'])
                my_list.append(s['DBSecurityGroupDescription'])
                my_list.append(s)
                menu[counter]=my_list


            print('#######################')
            print('Select Security Group')
            print('#######################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])+' - '+str(menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        name = menu[int(ans)][0]
                        break

            menu = {
                1:['Only CIDR Block or IP'],
                2:['EC2 Seucrity Group'],
                3:['EC2 Security Group and CIDR Bloc']
            }

            print("\n")
            print('##############################')
            print('Select Security Group Option')
            print('###############################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        selection = int(ans)
                        break


            if selection ==1:

                cidr = raw_input("Enter IP or CIDR Block in the format 192.168.0.0/16: [ENTER]")

                response = client.authorize_db_security_group_ingress(
                    DBSecurityGroupName=name,
                    CIDRIP=cidr
                )

                print("\n")
                print(pretty(response))

            elif selection ==2:

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
                        my_list.append(s['Description'])
                        my_list.append(s)
                        my_list.append(s['GroupId'])
                        my_list.append(s['OwnerId'])
                        menu[counter] = my_list

                    print "\n\n"
                    print '#########################################'
                    print '## Select Security Group               ##'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                ec2_name = menu[int(ans)][0]
                                id = menu[int(ans)][3]
                                owner_id = menu[int(ans)][4]
                                break

                    client = session.client('rds')
                    response = client.authorize_db_security_group_ingress(
                        DBSecurityGroupName=name,
                        EC2SecurityGroupId=id,
                        EC2SecurityGroupOwnerId=owner_id
                    )

                    print(pretty(response))

                else:
                    print("\n")
                    print("##############################")
                    print("No Security Groups Available")
                    print("##############################")
            else:


                cidr = raw_input("Enter IP or CIDR Block in the format 192.168.0.0/16: [ENTER]")

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
                        my_list.append(s['Description'])
                        my_list.append(s)
                        my_list.append(s['GroupId'])
                        my_list.append(s['OwnerId'])
                        menu[counter] = my_list

                    print "\n\n"
                    print '#########################################'
                    print '## Select Security Group               ##'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                ec2_name = menu[int(ans)][0]
                                id = menu[int(ans)][3]
                                owner_id = menu[int(ans)][4]
                                break

                    client = session.client('rds')
                    response = client.authorize_db_security_group_ingress(
                        DBSecurityGroupName=name,
                        CIDRIP='string',
                        EC2SecurityGroupName=ec2_name,
                        EC2SecurityGroupId=id,
                        EC2SecurityGroupOwnerId=owner_id
                    )

                    print(pretty(response))

                else:
                    print("\n")
                    print("##############################")
                    print("No Security Groups Available")
                    print("##############################")


        else:
            print("\n")
            print("########################")
            print('No RDS Security Groups')
            print("########################")
    else:
        print("\n")
        print("########################")
        print('No RDS Security Groups')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
