#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')


    response = client.describe_reserved_cache_nodes()

    if 'ReservedCacheNodes' in response:

        stacks = response['ReservedCacheNodes']

        if len(stacks):

            menu = {}
            counter=0
            for i in stacks:
                counter+=1
                my_list=[]
                my_list.append(i['ReservedCacheNodeId'])
                my_list.append(i['ProductDescription'])
                my_list.append(i)
                menu[counter]=my_list

            print "\n"
            print '#########################################'
            print '## Select Cache Reserved Node          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]+' - '+str(menu[key][1])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][2]
                        break

            print("\n")
            print("#######################################")
            print("Detailed Cache Reserved Node Info")
            print("#######################################")
            print(pretty(info))

        else:
            print("\n")
            print("#############################")
            print("No Cache Reserved Nodes")
            print("#############################")

    else:
        print("\n")
        print("#############################")
        print("No Cache Reserved Nodes")
        print("#############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
