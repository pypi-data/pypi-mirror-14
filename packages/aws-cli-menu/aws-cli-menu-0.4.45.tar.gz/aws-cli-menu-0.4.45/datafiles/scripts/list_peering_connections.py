#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    peering_connections = get_peering_connections(session)

    if (len(peering_connections) > 0):

        print("\n")

        menu = {}
        counter =0
        for pc in peering_connections:
            counter+=1
            my_list = []
            my_list.append(pc['pc_id'])

            if 'tags' in pc:
                if 'Value' in pc['tags']:
                    my_list.append(pc['tags']['Value'])
                else:
                    my_list.append('no tag')
            else:
                my_list.append('no tag')
            my_list.append(pc['status_code'])
            my_list.append(pc)
            menu[counter] = my_list



        print("\n")
        print("##########################")
        print("Select Peering Connection")
        print("##########################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0]) + ' - '+str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    code = menu[int(ans)][2]
                    info = menu[int(ans)][3]
                    break


        if code == 'deleted':
            print("\n")
            print '#############################'
            print 'Deleted Peering Connection'
            print '#############################'

        print("\n")
        print("##########################")
        print("Peering Connection")
        print("##########################")

        print(pretty(info))

    else:
        print("\n")
        print("################################")
        print('No peering connections found')
        print("################################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
