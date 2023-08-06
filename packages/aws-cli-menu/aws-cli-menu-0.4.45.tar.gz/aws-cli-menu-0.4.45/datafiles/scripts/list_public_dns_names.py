#!/usr/bin/env python

import boto3.session
import re
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

        # Get the data and store in an array and put in dictionary for sorting
        for s in stacks:
            name = s.get('Instances')[0]['Tags'][0]['Value']

            # An array for the data stored in the dictionary
            temp = []
            temp.append(str(name))
            temp.append(str(s.get('Instances')[0]['InstanceId']))
            temp.append(s.get('Instances')[0]['PublicDnsName'])

            data[str(name)] = temp

        sorted_array = []

        # Sort the dictionary items and put in new array
        for key, value in sorted(data.items()):
            sorted_array.append(value)

        labels = ('Name', 'ID', 'DNS Name')

        width = 20
        print indent([labels] + sorted_array, hasHeader=True, separateRows=True,
                     prefix='| ', postfix=' |',
                     wrapfunc=lambda x: wrap_always(x, width))

    else:
        print("\n")
        print("###############################")
        print('No public dns names found')
        print("###############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
