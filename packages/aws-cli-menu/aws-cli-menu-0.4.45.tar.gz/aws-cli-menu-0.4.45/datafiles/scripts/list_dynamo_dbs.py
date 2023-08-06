#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('dynamodb')

    response = client.list_tables()
    stacks = response.get('TableNames')

    if len(stacks) > 0:

        menu = {}
        counter=0
        for item in stacks:
            counter+=1
            menu[counter] = item


        print "\n"
        print '###############################'
        print '## Tables                    ##'
        print '###############################'
        for key in sorted(menu):
            print str(key)+": " + str(menu[key])




    else:
        print("\n")
        print("###############")
        print('No tables')
        print("###############")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
