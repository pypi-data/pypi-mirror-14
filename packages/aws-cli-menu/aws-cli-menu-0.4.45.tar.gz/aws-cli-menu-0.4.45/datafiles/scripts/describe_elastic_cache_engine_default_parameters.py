#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')


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
                my_list.append(i['CacheParameterGroupFamily'])
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
                        group_family = menu[int(ans)][2]
                        break

            response = client.describe_engine_default_parameters(
                CacheParameterGroupFamily=group_family
            )

            if 'EngineDefaults' in response:
                stacks = response['EngineDefaults']

                if len(stacks)>0:
                    print("\n")
                    print("###################")
                    print("Engine Defaults")
                    print("###################")
                    print(pretty(stacks))

                else:
                    print("\n")
                    print("######################")
                    print("No Engine Defaults")
                    print("######################")

            else:
                print("\n")
                print("######################")
                print("No Engine Defaults")
                print("######################")

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
