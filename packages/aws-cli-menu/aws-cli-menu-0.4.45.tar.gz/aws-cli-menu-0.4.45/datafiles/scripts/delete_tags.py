#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)


    resources = [
        'EC2 Instance', # 2
        'Dhcp-Options', # 1
        'Internet Gateway', # 3
        'Route-Table', # 4
        'Security Group', # 5
        'Snapshot', # 6
        'Subnet', # 7
        'Volume', # 8
        'VPC' #9
    ]

    menu = {}
    counter = 0
    for i in sorted(resources):
        counter += 1
        menu[counter] = i

    print("\n")
    print("###################################")
    print("Select Resource To Tag")
    print("###################################")
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if ans:
            if int(ans) in menu:
                answer = int(ans)
                break



    if answer == 2:
        print("\n")
        print('Getting ec2 instance ids...')
        instance_id = select_instance_id(session)

        answer = are_there_instance_tags(session, instance_id)


        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,instance_id,key,value)
        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")

    elif answer == 8:
        print("\n")
        print('Getting vpc ids...')

        vpc_id = select_vpc_id(session)

        answer = are_there_vpc_tags(session, vpc_id)

        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,vpc_id,key,value)
        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")


    elif answer == 7:
        print("\n")
        print('Getting subnet ids...')
        subnet_id = select_subnet_id(session)

        answer = are_there_subnet_tags(session, subnet_id)

        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,subnet_id,key,value)
        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")


    elif answer == 5:
        print("\n")
        print('Getting security group ids....')
        security_group_id = select_security_group_id(session)

        answer = are_there_security_group_tags(session, security_group_id)

        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,security_group_id,key,value)
        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")



    elif answer == 4:
        print("\n")
        print('Getting route table ids....')
        route_table_id = select_route_table_id(session)

        answer = are_there_route_table_tags(session, route_table_id)

        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,route_table_id,key,value)


        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")


    elif answer == 3:
        print("\n")
        print('Getting internet gateway ids....')
        internet_gateway_id = select_internet_gateway_id(session)

        answer = are_there_internet_gateway_tags(session, internet_gateway_id)

        if answer[0] is True:
            tags = answer[1]

            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,internet_gateway_id,key,value)


        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")


    elif answer == 6:
        print("\n")
        print('Getting snapshot ids...')
        snapshot_id = select_snapshot_id(session)

        answer = are_there_snapshot_tags(session, snapshot_id)

        if answer[0] is True:
            tags = answer[1]


            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,snapshot_id,key,value)


        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")


    elif answer == 1:
        print("\n")
        print('Getting dhcp-option ids....')
        dhcp_options_id = select_dhcp_option_id(session)

        answer = are_there_dhcp_options_tags(session, dhcp_options_id)

        if answer[0] is True:
            tags = answer[1]


            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,dhcp_options_id,key,value)


        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")



    elif answer ==9:
        print("\n")
        print('Getting volume ids...')
        volume_id = select_volume_id(session)

        answer = are_there_volume_tags(session, volume_id)

        if answer[0] is True:
            tags = answer[1]


            menu = {}
            counter =0
            for i in tags:
                counter+=1
                my_list= []
                my_list.append(i['Key'])
                my_list.append(i['Value'])
                menu[counter]=my_list

            print("\n")
            print("###################################")
            print("Select Tag To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+'- '+menu[key][1]

            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if ans:
                    if int(ans) in menu:
                        key = menu[int(ans)][0]
                        value = menu[int(ans)][1]
                        break

            delete_tags(session,volume_id,key,value)

        else:
            print("\n")
            print("#################")
            print('There are no tags')
            print("#################")




except (KeyboardInterrupt, SystemExit):
    sys.exit()
