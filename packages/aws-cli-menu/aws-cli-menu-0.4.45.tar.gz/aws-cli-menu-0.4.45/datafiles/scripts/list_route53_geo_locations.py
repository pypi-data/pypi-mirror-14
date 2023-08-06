#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('route53')

    response = client.list_geo_locations()

    if 'GeoLocationDetailsList' in response:

        stacks = response['GeoLocationDetailsList']
        print("\n")
        print("##################")
        print("Geo Locations")
        print("##################")
        for i in stacks:
            print(pretty(i))

    else:
        print("\n")
        print("##########################")
        print("No Geo Locations Lists.")
        print("##########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
