#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('elasticache')

    print("\n")
    name = raw_input("Enter new parameter group name: [ENTER]")

    print("\n")
    description = raw_input("Enter new parameter group description: [ENTER]")

    family=[
        'memcached1.4',
        'redis2.6',
        'redis2.8'
    ]

    menu = {}
    counter=0
    for i in sorted(family):
        counter+=1
        menu[counter]=i

    print "\n"
    print '#########################################'
    print '## Select Parameter Group Family'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                family = menu[int(ans)]
                break


    response = client.create_cache_parameter_group(
        CacheParameterGroupName=name,
        CacheParameterGroupFamily=family,
        Description=description
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
