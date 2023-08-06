#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_instances()
    stacks = response.get('Reservations')

    if len(stacks) > 0:

        data = {}

        for s in stacks:

            if 'PublicIpAddress' in s.get('Instances')[0].keys():

                # An array for the data stored in the dictionary
                temp = []
                temp.append(s.get('Instances')[0]['PublicIpAddress'])

                tags_array = []

                if 'Tags' in s['Instances'][0]:
                    tags = s.get('Instances')[0]['Tags']
                    for item in tags:
                        if isinstance(item, dict):
                            tags_array.append(str(item['Value']))
                else:
                    tags_array.append('No tags')

                temp.append(tags_array)

                data[s.get('Instances')[0]['PublicIpAddress']] = temp

        sorted_array = []

        if len(data)>0:
            # Sort the dictionary items and put in new array
            for key, value in sorted(data.items()):
                sorted_array.append(value)

            labels = ('Public IP', 'Tags')

            width = 40
            print indent([labels] + sorted_array, hasHeader=True, separateRows=True,
                     prefix='| ', postfix=' |',
                     wrapfunc=lambda x: wrap_always(x, width))
        else:
            print("\n")
            print"########################"
            print("No Public IPs Assigned")
            print("#######################")

    else:
        print("\n")
        print("########################")
        print('No Public IPs Found')
        print("########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
