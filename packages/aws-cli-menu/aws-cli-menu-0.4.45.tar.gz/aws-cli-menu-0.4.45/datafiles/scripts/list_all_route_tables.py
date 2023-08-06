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

    counter = 0
    if len(stacks)>0:
        for s in stacks:
            counter+=1
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

                    else:
                        list.append('none')
                else:
                    list.append('none')
            else:
                list.append('none')

            list.append(s)

            menu[counter] = list

        print "\n\n"
        print '#############################'
        print '## Select Route Table      ##'
        print '#############################'
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][1] + ' - '+str(menu[key][0]))+'- Associaton ID: '+str(menu[key][2])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    route_table_id = menu[int(ans)][1]
                    info = menu[int(ans)][3]
                    break


        print("\n")
        print("##########################")
        print("Detailed Route Table Info")
        print("##########################")
        print(pretty(info))


    else:
        print("\n")
        print("##########################")
        print('No route tables found')
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
