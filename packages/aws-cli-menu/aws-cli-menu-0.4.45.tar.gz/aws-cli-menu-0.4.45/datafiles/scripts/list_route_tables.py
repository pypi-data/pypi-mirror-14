#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    print("\n")
    print('** Please wait 10-15 seconds while we collect the information')

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
    response = client.describe_route_tables()
    stacks = response.get('RouteTables')

    menu = {}
    fields = {}
    counter=0
    for s in stacks:
        list=[]
        name = None
        id = str(s.get('RouteTableId'))

        if 'Tags' in s:

            if len(s.get('Tags'))>0:
                tags = s.get('Tags')

                if len(tags) > 1:
                    name = tags[0]
            else:
                name = 'no tags - '+str(id)

        vpc_id = str(s.get('VpcId'))
        vpc_name = get_vpc_name(session,vpc_id)

        if name:
            if 'Value' in name:
                list.append(name['Value'])
            else:
                list.append(name)
        else:
            list.append(vpc_name)

        list.append(id)
        if 'Associations' in s:

            if len(s['Associations'])>0:
                if 'RouteTableAssociationId' in s['Associations'][0]:
                    list.append(s['Associations'][0]['RouteTableAssociationId'])
                    list.append(str(s['Associations'][0]['Main']))
                    counter+=1
                else:
                    continue
            else:
                continue
        else:
            continue

        list.append(s)
        menu[counter] = list


    if len(menu) > 0:
        print_route_table_menu(menu)
        ans = raw_input("Make A Choice: [ENTER]")
        print"\n\n"
        route_table_name = menu[int(ans)][1]

        s = get_route_table_info(session, route_table_name)

        print "\n\n"
        print '#############################'
        print '## Route Table Info               ##'
        print '#############################'

        print(pretty(s))
    else:
        print("\n")
        print("##########################")
        print('No route tables found')
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
