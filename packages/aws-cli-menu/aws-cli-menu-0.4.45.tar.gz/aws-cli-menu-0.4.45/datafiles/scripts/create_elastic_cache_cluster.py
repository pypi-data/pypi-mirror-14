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
    name = raw_input("Enter new cluster name: [ENTER]")

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


    # Get node type
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

    print("\n")
    num_nodes = int(raw_input("Enter the number of nodes: [ENTER]"))


    response = client.describe_cache_parameter_groups()


    if 'CacheParameterGroups' in response:

        stacks = response['CacheParameterGroups']

        if len(stacks):

            menu = {}
            counter=0
            for i in stacks:
                counter+=1
                my_list=[]
                my_list.append(i['CacheParameterGroupName'])
                my_list.append(i)
                menu[counter]=my_list

            print "\n"
            print '#########################################'
            print '## Select Cache Parameter Group        ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        param_group_name = menu[int(ans)][0]
                        break



            # Select availability zone

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

            client = session.client('elasticache')
            response = client.create_cache_cluster(
                CacheClusterId=name,
                Engine=selected_engine_type,
                CacheNodeType=selected_node_type,
                NumCacheNodes=num_nodes,
                CacheParameterGroupName=param_group_name,
                PreferredAvailabilityZone=zones_ans,
                PreferredAvailabilityZones=[zones_ans]
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
            print("##########################")
            print("No Cache Parameter Groups")
            print("##########################")

    else:
        print("\n")
        print("##########################")
        print("No Cache Parameter Groups")
        print("##########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
