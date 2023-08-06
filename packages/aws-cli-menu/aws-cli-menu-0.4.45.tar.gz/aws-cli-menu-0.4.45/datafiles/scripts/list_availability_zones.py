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


    dict = {}
    if len(stacks) > 0:

        data = {}
        for s in stacks:

            if 'InstanceId' in s.get('Instances')[0].keys():

                # An array for the data stored in the dictionary
                temp = []
                if 'Tags' in s['Instances'][0]:
                    temp.append(s.get('Instances')[0]['Tags'][0]['Value'])
                else:
                    temp.append('no tags')

                temp.append(s.get('Instances')[0]['InstanceId'])
                temp.append(
                    s.get('Instances')[0]['Placement']['AvailabilityZone'])

                if 'Tags' in s['Instances'][0]:
                    data[s.get('Instances')[0]['Tags'][0]['Value']] = temp
                else:
                    data['no tags'] = temp

        sorted_array = []

        # Sort the dictionary items and put in new array
        for key, value in sorted(data.items()):
            sorted_array.append(value)

        labels = ('Instance Name', 'ID', 'Availability Zone')

        width = 40
        print indent([labels] + sorted_array, hasHeader=True, separateRows=True,
                     prefix='| ', postfix=' |',
                     wrapfunc=lambda x: wrap_always(x, width))

    else:
        print("\n")
        print("############################")
        print('No availability zones')
        print("############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
