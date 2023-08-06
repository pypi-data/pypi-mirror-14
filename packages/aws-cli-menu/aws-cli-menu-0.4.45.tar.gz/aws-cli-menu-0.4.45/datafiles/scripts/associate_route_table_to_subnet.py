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
            name = s.get('Tags')[0]['Value']
        else:
            name = 'no tags - ' + str(vpcid)

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

        client = session.client('ec2')

        response = client.describe_subnets()
        stacks = response.get('Subnets')

        menu = {}
        counter = 0
        for s in stacks:

            if s['VpcId'] == vpc_id:
                counter += 1
                my_list = []
                my_list.append(s['SubnetId'])
                my_list.append(s['CidrBlock'])
                my_list.append(s['State'])
                menu[counter]=my_list

        print "\n\n"
        print '#############################'
        print '## Select Subnet           ##'
        print '#############################'
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0] + ' - '+str(menu[key][1]))+' - '+str(menu[key][2])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    subnet_id = menu[int(ans)][0]
                    break




        client = session.client('ec2')
        response = client.describe_route_tables()
        stacks = response.get('RouteTables')

        menu = {}

        counter = 0
        if len(stacks)>0:
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
                            print('###'+str(s['Associations'][0]['RouteTableAssociationId']))
                            list.append(s['Associations'][0]['RouteTableAssociationId'])
                            continue
                        else:
                            list.append('none')
                            counter+=1
                    else:
                        list.append('none')
                        counter+=1
                else:
                    list.append('none')
                    counter+=1

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
                        route_tble_assoc_id = menu[int(ans)][2]
                        break


            response = client.associate_route_table(
                DryRun=False,
                SubnetId=subnet_id,
                RouteTableId=route_table_id
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("############################")
            print("There are no route tables")
            print("############################")

    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
