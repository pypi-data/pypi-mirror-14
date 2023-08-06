#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_spot_price_history(
        DryRun=False
    )

    if 'SpotPriceHistory' in response:
        stacks = response.get('SpotPriceHistory')

        if len(stacks) > 0:


            counter=0
            for s in stacks:
                counter+=1
                print "\n"
                print '#########################################'
                print '## Spot History #'+str(counter)
                print '#########################################'
                print(pretty(s))


        else:
            print("\n")
            print("##########################")
            print('No Spot Price History')
            print("#########################")
    else:
        print("\n")
        print("###########################")
        print('No Spot Price History')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
