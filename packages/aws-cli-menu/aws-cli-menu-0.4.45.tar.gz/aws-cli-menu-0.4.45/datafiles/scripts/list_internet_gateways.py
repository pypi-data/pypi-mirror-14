#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    internet_gateways = []

    for internet_gateways_iterator in client.internet_gateways.all():

        ig = {}

        ig_id = internet_gateways_iterator.id

        ig['ig_id']= ig_id


        tags = internet_gateways_iterator.tags

        if len(tags) >0:
            ig['tags'] = tags
        else:
            ig['tags']= []

        internet_gateways.append(ig)

    if (len(internet_gateways) > 0):

        menu = {}
        counter =0
        for ig in internet_gateways:
            counter+=1
            my_list = []
            my_list.append(ig['ig_id'])
            if 'tags' in ig:
                if 'Value' in ig['tags']:
                    my_list.append(ig['tags']['Value'])
                else:
                    my_list.append('no tags')
            else:
                my_list.append('no tags')

            my_list.append(ig)
            menu[counter]=my_list

        print("\n")
        print("#########################")
        print("Select Internet Gateway")
        print("#########################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0])+str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    info = menu[int(ans)][2]
                    break
        print("\n")
        print("########################")
        print("Internet Gateway Info")
        print("#######################")
        print(pretty(info))

    else:
        print("\n")
        print("##############################")
        print('No internet gateways found')
        print("##############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
