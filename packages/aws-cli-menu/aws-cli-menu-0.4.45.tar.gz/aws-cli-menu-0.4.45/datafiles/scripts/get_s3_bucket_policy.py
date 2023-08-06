#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import yaml


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('s3')
    response = client.list_buckets()
    stacks = response.get('Buckets')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for s in stacks:
            counter += 1
            menu[counter] = s['Name']

        print "\n\n"
        print '#########################################'
        print '## Select Object                       ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    object_name = menu[int(ans)]
                    break

        response = client.get_bucket_policy(
            Bucket=object_name
        )

        policy = response['Policy']
        d = yaml.load(policy)
        print("\n")
        print("##########################")
        print("Policy is:")
        print("##########################")
        print(pretty(d))

    else:
        print("\n")
        print("#########################")
        print('No S3 buckets found')
        print("#########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
