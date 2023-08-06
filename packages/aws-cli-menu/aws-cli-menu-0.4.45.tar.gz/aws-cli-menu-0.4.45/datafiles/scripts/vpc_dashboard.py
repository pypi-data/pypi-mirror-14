#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")


    session = boto3.session.Session(profile_name=profile_name)

    print("\n")
    print("** Please wait 5-10 seconds while we collect the information. **")

    menu = {
        1:['VPCs',[0]],
        2:['Subnets',[0]],
        3:['Network ACLs',[0]],
        4:['VPC Peering Connections',[0]],
        5:['Placement Groups',[0]],
        6:['Nat Gateways',[0]],
        7:['Running Instances',[0]],
        8:['Virtual Private Gateways',[0]],
        9:['Internet Gateways',[0]],
        10:['Route Tables',[0]],
        11:['Elastic IPs',[0]],
        12:['Security Groups',[0]],
        13:['VPN Connections',[0]],
        14:['Customer Gateways',[0]]
    }

    #1 Get VPCs
    client = session.client('ec2')
    response = client.describe_vpcs()

    sub_menu = {}
    if 'Vpcs' in response:

        stacks = response.get('Vpcs')

        if len(stacks) > 0:


            counter = 0
            for s in stacks:
                counter+=1
                my_list = []

                if 'Tags' in s:
                    name = 'Tag: '+str(s['Tags'][0]['Value'])
                else:
                    name = 'Tag: None - ' + str(s.get('VpcId'))
                vpcid = s.get('VpcId')
                cidr_block = s.get('CidrBlock')

                my_list.append(name)
                my_list.append(vpcid)
                my_list.append(cidr_block)
                my_list.append(s)
                sub_menu[counter] = my_list


    if len(sub_menu)>0:
        menu[1][1][0] = int(len(sub_menu))
        menu[1][1].append(sub_menu)


    #2 Get Subnets

    client = session.client('ec2')
    response = client.describe_subnets()
    stacks = response.get('Subnets')

    sub_menu = {}

    counter = 0
    for s in stacks:
        counter+=1
        list=[]

        id = str(s.get('SubnetId'))

        vpc_id = s.get('VpcId')

        vpc_name = get_vpc_name(session,vpc_id)

        cidr_block = s.get('CidrBlock')

        list.append(vpc_name)
        list.append(id)
        list.append(cidr_block)
        sub_menu[counter] = list

    if len(sub_menu)>0:
        menu[2][1][0] = int(len(sub_menu))
        menu[2][1].append(sub_menu)



    #3 Get Network ACLs
    client = session.resource('ec2')

    network_acls = []
    sub_menu = {}
    for network_acl_iterator in client.network_acls.all():

        acl = {}

        acl_id = network_acl_iterator.id


        client2 = session.client('ec2')
        response = client2.describe_network_acls(
            DryRun=False,
            NetworkAclIds=[acl_id]
        )

        stacks = response.get('NetworkAcls')

        if len(stacks) > 0:


            counter =0
            for s in stacks:
                counter+=1

                my_list = []
                my_list.append(s['NetworkAclId'])
                if len(s['Tags'])>0:
                    my_list.append(s['Tags'])
                else:
                    my_list.append('None')

                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[3][1][0] = int(len(sub_menu))
        menu[3][1].append(sub_menu)




    #4 VPC Peering Connections
    client = session.resource('ec2')

    peering_connections = []
    sub_menu = {}
    for vpc_peering_connection_iterator in client.vpc_peering_connections.all():

        pc = {}

        vpc_pc_id = vpc_peering_connection_iterator.id

        pc['pc_id']= vpc_pc_id


        accepter_owner_id = vpc_peering_connection_iterator.accepter_vpc_info['OwnerId']
        accepter_vpc_id = vpc_peering_connection_iterator.accepter_vpc_info['VpcId']

        pc['accepter_owner_id'] = accepter_owner_id
        pc['accepter_vpc_id'] = accepter_vpc_id


        requester_owner_id = vpc_peering_connection_iterator.requester_vpc_info['OwnerId']
        requester_vpc_id = vpc_peering_connection_iterator.requester_vpc_info['VpcId']
        requester_cidr_block = vpc_peering_connection_iterator.requester_vpc_info['CidrBlock']

        pc['requester_owner_id']=requester_owner_id
        pc['requester_vpc_id'] = requester_vpc_id
        pc['requester_cidr_block'] = requester_cidr_block


        status = vpc_peering_connection_iterator.status['Message']
        status_code = vpc_peering_connection_iterator.status['Code']

        pc['status'] = status
        pc['status_code'] = status_code

        tags = vpc_peering_connection_iterator.tags

        if len(tags) >0:
            pc['tags'] = tags
        else:
            pc['tags']= []


        peering_connections.append(pc)

        if (len(peering_connections) > 0):

            counter =0
            for pc in peering_connections:
                counter+=1
                my_list = []
                my_list.append(pc['pc_id'])

                if 'tags' in pc:
                    if 'Value' in pc['tags']:
                        my_list.append(pc['tags']['Value'])
                    else:
                        my_list.append('no tag')
                else:
                    my_list.append('no tag')
                my_list.append(pc['status_code'])
                my_list.append(pc)
                sub_menu[counter] = my_list


    if len(sub_menu)>0:
        menu[4][1][0] = int(len(sub_menu))
        menu[4][1].append(sub_menu)


    #5 Placement Groups

    client = session.client('ec2')


    response = client.describe_placement_groups(
        DryRun=False
    )

    stacks = response.get('PlacementGroups')
    sub_menu= {}
    if len(stacks)>0:


        counter=0
        for i in stacks:
            counter+=1
            my_list = []
            my_list.append(i['GroupName'])
            my_list.append(i)
            sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[5][1][0] = int(len(sub_menu))
        menu[5][1].append(sub_menu)





    #6 Nat Gateways

    client = session.client('ec2')
    response = client.describe_nat_gateways()

    stacks = response.get('NatGateways')
    sub_menu={}
    if len(stacks) > 0:

        counter = 0
        for i in stacks:

            if i['State'] != 'deleted':
                counter += 1
                my_list = []
                my_list.append(i['NatGatewayId'])
                my_list.append(i['SubnetId'])
                my_list.append(i['VpcId'])
                my_list.append(i)
                sub_menu[counter] = my_list


    if len(sub_menu)>0:
        menu[6][1][0] = int(len(sub_menu))
        menu[6][1].append(sub_menu)



    #7 Get Running Instances
    client = session.client('ec2')
    response = client.describe_instances()

    stacks = response.get('Reservations')

    sub_menu = {}
    counter = 0
    for s in stacks:

        my_list=[]

        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:
            name = s.get('Instances')[0]['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        my_list.append(name)
        my_list.append(s['Instances'][0]['InstanceId'])

        if 'State' in s['Instances'][0]:
            state = s['Instances'][0]['State']['Name']
        else:
            state = 'none'

        if state == 'running':
            counter+=1
            my_list.append(state)
            sub_menu[counter] = my_list


    if len(sub_menu)>0:
        menu[7][1][0] = int(len(sub_menu))
        menu[7][1].append(sub_menu)



    # 8 Get Virtual Private Gateways




    # 9 Get Internet Gateways

    client = session.resource('ec2')

    internet_gateways = []

    for internet_gateways_iterator in client.internet_gateways.all():

        ig = {}

        ig_id = internet_gateways_iterator.id

        ig['ig_id']= ig_id


        tags = internet_gateways_iterator.tags

        if len(tags) >0:
            ig['tags'] = tags
        else:
            ig['tags']= []

        internet_gateways.append(ig)

    sub_menu={}
    if (len(internet_gateways) > 0):

        counter =0
        for ig in internet_gateways:
            counter+=1
            my_list = []
            my_list.append(ig['ig_id'])
            if 'tags' in ig:
                if 'Value' in ig['tags']:
                    my_list.append(ig['tags']['Value'])
                else:
                    my_list.append('no tags')
            else:
                my_list.append('no tags')

            my_list.append(ig)
            sub_menu[counter]=my_list



    if len(sub_menu)>0:
        menu[9][1][0] = int(len(sub_menu))
        menu[9][1].append(sub_menu)



    # 10 Get Route Tables

    client = session.client('ec2')
    response = client.describe_route_tables()
    stacks = response.get('RouteTables')

    sub_menu = {}
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
        sub_menu[counter] = list


    if len(sub_menu)>0:
        menu[10][1][0] = int(len(sub_menu))
        menu[10][1].append(sub_menu)




    # 11 Get Elastic IPs

    client = session.client('ec2')
    response = client.describe_addresses()
    elastic_ips = response.get('Addresses')

    sub_menu= {}
    if len(elastic_ips) > 0:


        counter =0
        for e in elastic_ips:
            counter +=1
            my_list = []
            my_list.append(e['AllocationId'])
            my_list.append(e['PublicIp'])
            my_list.append(e)
            sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[11][1][0] = int(len(sub_menu))
        menu[11][1].append(sub_menu)


    # 12 Get Security Groups

    client = session.client('ec2')
    response = client.describe_security_groups()
    stacks = response.get('SecurityGroups')

    sub_menu = {}
    if len(stacks) > 0:

        counter = 0
        for s in stacks:
            counter += 1
            my_list = []
            my_list.append(s['GroupName'])
            my_list.append(s['Description'])
            my_list.append(s)
            sub_menu[counter] = my_list

    if len(sub_menu)>0:
        menu[12][1][0] = int(len(sub_menu))
        menu[12][1].append(sub_menu)

    # 13 Get VPN Connections

    client = session.client('ec2')
    response = client.describe_vpn_connections(
        DryRun=False
    )

    stacks = response.get('VpnConnections')
    sub_menu={}
    if len(stacks)>0:

        menu = {}
        counter=0
        for s in stacks:
            counter+=1
            my_list=[]

            my_list.append(s['VpnConnectionId'])
            my_list.append(s['State'])
            my_list.append(s)
            sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[13][1][0] = int(len(sub_menu))
        menu[13][1].append(sub_menu)


    # 14 Get Customer Gateways

    client = session.client('ec2')
    response = client.describe_customer_gateways(
        DryRun=False
    )

    sub_menu = {}
    if 'CustomerGateways' in response:

        stacks = response['CustomerGateways']

        if (len(stacks) > 0):

            counter=0
            for ig in stacks:

                if ig['State'] <> 'deleted':
                    counter+=1
                    my_list=[]
                    my_list.append(ig['CustomerGatewayId'])
                    my_list.append(ig['IpAddress'])
                    my_list.append(ig['State'])
                    my_list.append(ig)
                    sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[14][1][0] = int(len(sub_menu))
        menu[14][1].append(sub_menu)





    print("\n")
    print("######################")
    print("VPC Dashboard")
    print("######################")
    for key in sorted(menu):
        print str(key)+":" + str(menu[key][0]) + ' - '+str(menu[key][1][0])

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                results = menu[int(ans)]
                break

    if len(results[1])>1:
        menu_title = results[0]
        count = results[1][0]
        new_menu = results[1][1]



        # Get VPCs
        if int(ans) == 1:

            print "\n"
            print '#########################################'
            print '## Select VPC                          ##'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0]) + ' - ' + str(new_menu[key][1]) + ' - ' + str(new_menu[key][2])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        vpc_id = new_menu[int(ans)][1]
                        info = new_menu[int(ans)][3]
                        break
                    elif int(ans) ==0:
                        sys.exit(1)

            print "\n"
            print '#########################################'
            print '## VPC Details                         ##'
            print '#########################################'
            print(pretty(info))



        # Get Subnets
        elif int(ans) ==2:


            print_subnet_menu(new_menu)
            ans = raw_input("Make A Choice: [ENTER]")
            print"\n\n"
            instance_id = new_menu[int(ans)][1]

            info = get_subnet_info(session, instance_id)

            print "\n\n"
            print '#########################################'
            print '## Subnet Info                         ##'
            print '#########################################'

            print(pretty(info))

        # Get Network ACLs
        elif int(ans) ==3:


            print "\n"
            print '#############################'
            print '## Select Network ACL      ##'
            print '#############################'
            for key in sorted(new_menu):
                print str(key)+": Tags: " + str(new_menu[key][1]) + ' - '+str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("####################################")
            print("# Detailed Network ACL Info")
            print("####################################")
            print(pretty(info))

        # Get VPC Peering Connections
        elif int(ans) ==4:

            print("\n")
            print("##########################")
            print("Select Peering Connection")
            print("##########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0]) + ' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        code = new_menu[int(ans)][2]
                        info = new_menu[int(ans)][3]
                        break


            if code == 'deleted':
                print("\n")
                print '#############################'
                print 'Deleted Peering Connection'
                print '#############################'

            print("\n")
            print("##########################")
            print("Peering Connection")
            print("##########################")

            print(pretty(info))



        # Get Placement Groups
        elif int(ans) ==5:

            print("\n")
            print("##########################")
            print("Select Placement Groups")
            print("##########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][1]
                        break

            print("\n")
            print("##################################")
            print("Placement Group Information")
            print("##################################")
            print(pretty(info))



        # Get Nat Gateways
        elif int(ans) ==6:

            print "\n\n"
            print '#########################################'
            print '## Select NAT Gateway                  ##'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0]) + ' - ' + str(new_menu[key][1]) + ' - ' + str(new_menu[key][2])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][3]
                        break

            print("\n")
            print("####################################")
            print("Detailed NAT Gateway Information")
            print("####################################")

            print(pretty(info))


        # Running Instances
        elif int(ans) ==7:

            print("\n")
            print("#########################")
            print("Select Running Instance")
            print("#########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])+'- State: '+str(new_menu[key][2])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        instance_id = new_menu[int(ans)][1]
                        break

            info = get_instance_info(session, instance_id)

            print("\n")
            print("##################################")
            print("Instance Information")
            print("##################################")
            print(pretty(info))

        # Virtual Private Gateways
        elif int(ans) ==8:
            print('To be prepared')

        # Internet Gateways
        elif int(ans) ==9:

            print("\n")
            print("#########################")
            print("Select Internet Gateway")
            print("#########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break
            print("\n")
            print("########################")
            print("Internet Gateway Info")
            print("#######################")
            print(pretty(info))

        # Route Tables
        elif int(ans) ==10:
            print "\n"
            print '#############################'
            print '## Select Route Table      ##'
            print '#############################'
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][1] + ' - '+str(new_menu[key][0]))+'- Main Route Table: '+str(new_menu[key][3])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        rout_table_name = new_menu[int(ans)][1]
                        break

            s = get_route_table_info(session, route_table_name)

            print "\n"
            print '#############################'
            print '## Route Table Info'
            print '#############################'

            print(pretty(s))



        # Elastic IPs
        elif int(ans) ==11:

            print("\n")
            print("######################")
            print("Select Elastic IP")
            print("######################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0]) + ' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)]
                        break


            print('#########################')
            print('Detailed Elastic IP Info')
            print('#########################')
            print(pretty(info))




        # Security Groups
        elif int(ans) ==12:

            print "\n"
            print '#########################################'
            print '## Select Security Group               ##'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0]) + '-' + str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        answer = new_menu[int(ans)][2]
                        break

            print("\n")
            print("######################################")
            print("Detailed Security Group Information")
            print("######################################")

            print(pretty(answer))

        # VPN Connections
        elif int(ans) ==13:

            print("\n")
            print("##########################")
            print("Select VPN Connection")
            print("##########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])+' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break
        # Customer Gateways
        else:

            print "\n"
            print '#########################################'
            print '## Select Customer Gateway'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + new_menu[key][0] + ' - ' + new_menu[key][1] + ' - ' + new_menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][3]
                        break


            print("\n")
            print(pretty(info))



except (KeyboardInterrupt, SystemExit):
    sys.exit()
