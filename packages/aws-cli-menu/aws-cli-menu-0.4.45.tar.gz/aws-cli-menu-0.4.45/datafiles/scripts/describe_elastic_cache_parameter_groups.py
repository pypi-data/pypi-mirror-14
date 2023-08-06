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
                        info = menu[int(ans)][1]
                        break

            print("\n")
            print("##################################")
            print("Detailed Cache Parameter Group")
            print("##################################")
            print(pretty(info))

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
