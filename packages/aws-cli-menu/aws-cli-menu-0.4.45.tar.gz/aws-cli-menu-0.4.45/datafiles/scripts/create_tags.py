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
        'Network Interface', #4
        'Route-Table', # 5
        'Security Group', # 6
        'Snapshot', # 7
        'Subnet', # 8
        'Volume', # 9
        'VPC' #10
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
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_instance_tag(session, instance_id)

        print("\n")
        print(pretty(response))


    elif answer == 9:
        print("\n")
        print('Getting vpc ids...')

        vpc_id = select_vpc_id(session)

        if are_there_vpc_tags(session, vpc_id) is True:
            print('There are tags')
            tags = get_vpc_tags(session, vpc_id)
            print("######################")
            print("Current Tags")
            print("######################")
            print(tags)
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_vpc_tag(session, vpc_id)

        print("\n")
        print(pretty(response))

    elif answer == 8:
        print("\n")
        print('Getting subnet ids...')
        subnet_id = select_subnet_id(session)

        if are_there_subnet_tags(session, subnet_id) is True:
            print('There are tags')
            tags = get_subnet_tags(session, subnet_id)
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_subnet_tag(session, subnet_id)

        print("\n")
        print(pretty(response))

    elif answer == 6:
        print("\n")
        print('Getting security group ids....')
        security_group_id = select_security_group_id(session)

        answer = are_there_security_group_tags(session, security_group_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_security_group_tag(session, security_group_id)

        print("\n")
        print(pretty(response))


    elif answer == 5:
        print("\n")
        print('Getting route table ids....')
        route_table_id = select_route_table_id(session)

        answer = are_there_route_table_tags(session, route_table_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_route_table_tag(session, route_table_id)

        print("\n")
        print(pretty(response))


    elif answer == 3:
        print("\n")
        print('Getting internet gateway ids....')
        internet_gateway_id = select_internet_gateway_id(session)

        answer = are_there_internet_gateway_tags(session, internet_gateway_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_internet_gateway_tag(session, internet_gateway_id)

        print("\n")
        print(pretty(response))

    elif answer == 7:
        print("\n")
        print('Getting snapshot ids...')
        snapshot_id = select_snapshot_id(session)

        answer = are_there_snapshot_tags(session, snapshot_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_snapshot_tag(session, snapshot_id)

        print("\n")
        print(pretty(response))

    elif answer == 1:
        print("\n")
        print('Getting dhcp-option ids....')
        dhcp_options_id = select_dhcp_option_id(session)

        answer = are_there_dhcp_options_tags(session, dhcp_options_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_dhcp_options_tag(session, dhcp_options_id)

        print("\n")
        print(pretty(response))


    elif answer ==10:
        print("\n")
        print('Getting volume ids...')
        volume_id = select_volume_id(session)

        answer = are_there_volume_tags(session, volume_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_dhcp_options_tag(session, volume_id)

        print("\n")
        print(pretty(response))

    elif answer ==4:
        print("\n")
        print('Getting netwrok interface ids...')
        network_interface_id = select_network_interface_id(session)

        answer = are_there_network_interface_tags(session, network_interface_id)

        if answer[0] is True:
            print('There are tags')
            #print(answer[1])
            tags = answer[1]
            print("######################")
            print("Current Tags")
            print("######################")
            print(pretty(tags))
        else:
            print("\n")
            print("#####################")
            print('There are no tags')
            print("#####################")

        print("\n")
        print("#########################")
        print("Enter New Tag Information")
        print("#########################")
        response = create_network_interface_tag(session, network_interface_id)

        print("\n")
        print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
