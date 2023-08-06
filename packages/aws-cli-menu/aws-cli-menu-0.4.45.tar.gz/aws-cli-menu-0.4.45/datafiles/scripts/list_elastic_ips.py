#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)


    client = session.client('ec2')
    response = client.describe_addresses()
    elastic_ips = response.get('Addresses')

    if len(elastic_ips) > 0:

        menu = {}
        counter =0
        for e in elastic_ips:
            counter +=1
            my_list = []
            my_list.append(e['AllocationId'])
            my_list.append(e['PublicIp'])
            my_list.append(e)
            menu[counter]=my_list


        print("\n")
        print("######################")
        print("Select Elastic IP")
        print("######################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0]) + ' - '+str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    info = menu[int(ans)]
                    break


        print('#########################')
        print('Detailed Elastic IP Info')
        print('#########################')
        print(pretty(info))


    else:
        print("\n")
        print("########################")
        print('No elastic ips found')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
