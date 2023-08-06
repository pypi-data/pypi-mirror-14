#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_spot_instance_requests(
        DryRun=False
    )

    if 'SpotInstanceRequests' in response:
        stacks = response.get('SpotInstanceRequests')

        if len(stacks) > 0:


            counter=0
            for s in stacks:
                counter+=1
                print "\n"
                print '#########################################'
                print '## Spot Instance '+str(counter)
                print '#########################################'
                print(pretty(s))


        else:
            print("\n")
            print("##########################")
            print('No Spot Instance Request')
            print("#########################")
    else:
        print("\n")
        print("###########################")
        print('No Spot Instance Request')
        print("###########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
