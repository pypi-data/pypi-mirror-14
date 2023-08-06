#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:
    print('test')
    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.resource('ec2')

    internet_gateways = []

    for internet_gateways_iterator in client.internet_gateways.all():
        ig = {}

        ig_id = internet_gateways_iterator.id

        ig['ig_id'] = ig_id

        tags = internet_gateways_iterator.tags

        if len(tags) > 0:
            ig['tags'] = tags
        else:
            ig['tags'] = ['There are no tags for the vpc']

        internet_gateways.append(ig)

    menu = {}

    counter = 0
    for item in sorted(internet_gateways):
        counter = counter + 1
        menu[counter] = item['ig_id']

    if len(menu) > 0:
        print "\n\n"
        print '#########################################'
        print '## Select Internet Gateway To Delete   ##'
        print '#########################################'

        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    internet_gateway_id = menu[int(ans)]
                    break


        client = session.client('ec2')
        response = client.delete_internet_gateway(
            DryRun=False,
            InternetGatewayId=internet_gateway_id
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("################################")
        print('No internet gateways available')
        print("################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
