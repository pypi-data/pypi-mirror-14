#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    response = list_hosted_zones(session)

    stacks = response.get('HostedZones')

    if len(stacks)>0:

        menu = {}
        counter = 0
        for item in stacks:
            counter +=1
            my_list=[]
            my_list.append(item['Name'])
            my_list.append(item['Id'])
            menu[counter]=my_list


        print("\n")
        print("#################################")
        print("Select Hosted Zones")
        print("#################################")
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    id = menu[int(ans)][1]
                    break


        client = session.client('route53')
        response = client.list_resource_record_sets(
            HostedZoneId=id
        )

        if 'ResourceRecordSets' in response:

            print("\n")


            stacks = response['ResourceRecordSets']
            for i in stacks:
                print("###########################")
                print("Record Sets")
                print("###########################")
                print(pretty(i))

        else:
            print("\n")
            print("##################")
            print("No Record Sets")
            print("##################")
    else:
        print("\n")
        print("######################")
        print("No Hosted Zones")
        print("######################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
