#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')

    print("\n")
    name = raw_input("Enter new replication group name: [ENTER]")
    print("\n")
    description = raw_input("Enter replication group description: [ENTER]")

    print("\n")
    num_clusters = int(raw_input("Enter the number of clusters: [ENTER]"))

    engine_type=[
        'redis',
        'memcached'
    ]

    menu = {}
    counter=0
    for i in sorted(engine_type):
        counter+=1
        menu[counter]=i

    print "\n"
    print '#########################################'
    print '## Select Engine Type'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_engine_type = menu[int(ans)]
                break

    node_type = [

        'cache.t2.micro' ,
        'cache.t2.small' ,
        'cache.t2.medium' ,
        'cache.m3.medium' ,
        'cache.m3.large' ,
        'cache.m3.xlarge' ,
        'cache.m3.2xlarge'
        'cache.r3.large' ,
        'cache.r3.xlarge' ,
        'cache.r3.2xlarge' ,
        'cache.r3.4xlarge' ,
        'cache.r3.8xlarge'
    ]

    menu = {}
    counter=0
    for i in sorted(node_type):
        counter+=1
        menu[counter]=i

    print "\n"
    print '#########################################'
    print '## Select Node Type'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                selected_node_type = menu[int(ans)]
                break


   # Get availability zones
    client = session.client('ec2')
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

    for key in sorted(zones):
        print str(key) + ":" + zones[key]

    while True:

        ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
        if int(ans2) in zones:
            zones_ans = zones[int(ans2)]
            break

    failover = yes_or_no('Enable Automatic Failover')

    if failover == True and num_clusters<2:
        print("\n")
        print("Because failover is true, there must be 2 or more clusters.")
        print("\n")
        num_clusters = int(raw_input("Enter the number of clusters: [ENTER]"))


    # Select subnet


    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    for s in stacks:
        list = []

        vpcid = s.get('VpcId')

        if 'Tags' in s:
            name = 'Tag: '+str(s.get('Tags')[0]['Value'])
        else:
            name = 'Tag: None - ' + str(vpcid)

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

                menu={}
                counter = 0
                for s in stacks:

                    if s['VpcId'] == vpc_id:
                        counter += 1
                        my_list = []
                        my_list.append(s['SubnetId'])
                        my_list.append(s)
                        my_list.append(s['CidrBlock'])
                        my_list.append(s['State'])
                        my_list.append(s['DefaultForAz'])
                        menu[counter]=my_list


                if len(menu)>0:
                    print("\n")
                    print("####################################")
                    print("Select Subnet")
                    print("####################################")

                    for key in sorted(menu):
                        print str(key) + ":" + str(menu[key][0])+' - '+str(menu[key][2])+' - '+str(menu[key][3])

                    while True:

                        ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                        if int(ans2) in menu:
                            subnet_id = menu[int(ans2)][0]
                            info = menu[int(ans2)][1]
                            break

                    if selected_engine_type == 'memcached':
                        failover = False

                        client = session.client('elasticache')
                        response = client.create_replication_group(
                            ReplicationGroupDescription=description,
                            NumCacheClusters=num_clusters,
                            Engine=selected_engine_type,
                            CacheNodeType=selected_node_type,
                            PreferredCacheClusterAZs=[zones_ans ],
                            AutomaticFailoverEnabled = failover,
                            CacheSubnetGroupName=subnet_id
                        )


                        print("\n")
                        print(pretty(response))

                    else:

                        client = session.client('elasticache')
                        response = client.create_replication_group(
                            ReplicationGroupId=name,
                            ReplicationGroupDescription=description,
                            NumCacheClusters=num_clusters,
                            Engine=selected_engine_type,
                            CacheNodeType=selected_node_type,
                            PreferredCacheClusterAZs=[zones_ans ],
                            AutomaticFailoverEnabled = failover,
                            CacheSubnetGroupName = subnet_id
                        )


                        print("\n")
                        print(pretty(response))


                        print("\n")
                        print("###############################################################")
                        print("We are aware this function is not working in aws-cli-menu")
                        print("Hopefully, we can get it fixed soon")
                        print("##############################################################")



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
            print("#######################")
            print("No Subnets In This VPC")
            print("#######################")



    else:
        print("\n")
        print("############################")
        print('No vpc information found')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
