#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    cf_client = session.client('ec2')
    response = cf_client.describe_instances()
    stacks = response.get('Reservations')

    if len(stacks) > 0:
        data = {}

        if 'Instances' in stacks[0]:

            instances = stacks[0]['Instances']

            for s in instances:

                if 'PrivateIpAddress' in s:

                    # An array for the data stored in the dictionary
                    temp = []


                    temp.append(s['PrivateIpAddress'])

                    tags_array = []

                    if 'Tags' in s:
                        tags = s['Tags']
                        for item in tags:
                            if isinstance(item, dict):
                                tags_array.append(str(item['Value']))
                    else:
                        tags_array.append('None')

                    temp.append(tags_array)

                    data[s['PrivateIpAddress']] = temp

            sorted_array = []

            # Sort the dictionary items and put in new array
            for key, value in sorted(data.items()):
                sorted_array.append(value)

            labels = ('Private IP', 'Tags')

            width = 40
            print indent([labels] + sorted_array, hasHeader=True, separateRows=True,
                     prefix='| ', postfix=' |',
                     wrapfunc=lambda x: wrap_always(x, width))
        else:
            print("\n")
            print("###################")
            print("No Instances")
            print("###################")

    else:
        print("\n")
        print("#######################")
        print('No private ips found')
        print("#######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
