#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_key_pairs()

    if 'KeyPairs' in response:
        stacks = response.get('KeyPairs')

        if len(stacks) > 0:

            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list=[]
                my_list.append(s['KeyName'])
                my_list.append(s)
                menu[counter]=my_list

            print "\n"
            print '#########################################'
            print '## Select Key Pair'
            print '#########################################'
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern,ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][1]
                        break


            print("\n")
            print('#######################')
            print('Detailed Key Pair Info')
            print('#######################')
            print(pretty(info))

        else:
            print("\n")
            print("##################")
            print('No Key Pairs')
            print("##################")
    else:
        print("\n")
        print("##################")
        print('No Key Pairs')
        print("##################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
