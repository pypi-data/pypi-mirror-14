#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('apigateway')

    print("\n")
    name = raw_input("Enter name for the new API: [ENTER]")

    print("\n")
    description = raw_input("Enter API Description: [ENTER]")

    print("\n")
    clone = yes_or_no('Do You Want To Clone From An Existing API?')

    if clone == True:

        response = client.get_rest_apis()

        stacks = response.get('items')


        if len(stacks)>0:

            menu = {}
            counter=0

            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['name'])
                my_list.append(s['description'])
                my_list.append(s)
                my_list.append(s['id'])
                menu[counter]=my_list

            print "\n"
            print '#############################'
            print '## Select API To Clone From'
            print '#############################'
            for key in sorted(menu):
                print str(key)+":" + str(menu[key][0] + ' - '+str(menu[key][1]))

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        clone_name = menu[int(ans)][0]
                        id = menu[int(ans)][3]
                        break

            print('clone name: '+str(clone_name))
            response = client.create_rest_api(
                name=name,
                description=description,
                cloneFrom=id
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("#############################")
            print("No APIs Found To Clone From")
            print("Please Try Again.")
            print("#############################")

    else:

        response = client.create_rest_api(
            name=name,
            description=description
        )
        print("\n")
        print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
