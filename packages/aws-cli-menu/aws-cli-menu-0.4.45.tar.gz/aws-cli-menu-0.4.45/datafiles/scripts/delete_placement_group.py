#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')


    response = client.describe_placement_groups(
        DryRun=False
    )

    stacks = response.get('PlacementGroups')

    if len(stacks)>0:

        menu = {}
        counter=0
        for i in stacks:
            counter+=1
            my_list = []
            my_list.append(i['GroupName'])
            my_list.append(i)
            menu[counter]=my_list

        if len(menu) > 0:

            print("\n")
            print("###################################")
            print("Select Placement Groups To Delete")
            print("###################################")
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        name = menu[int(ans)][0]
                        break


            response = client.delete_placement_group(
                DryRun=False,
                GroupName=name
            )

            print("\n")
            print(pretty(response))

    else:
        print("\n\n")
        print('##############################')
        print('No placement groups found')
        print('##############################')

except (KeyboardInterrupt, SystemExit):
    sys.exit()
