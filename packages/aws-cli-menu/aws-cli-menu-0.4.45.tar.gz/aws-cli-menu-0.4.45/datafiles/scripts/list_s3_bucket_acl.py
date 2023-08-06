#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('s3')
    response = client.list_buckets()
    stacks = response.get('Buckets')

    if len(stacks) > 0:

        menu = {}
        names = []

        for s in stacks:
            name = s.get('Name')
            names.append(name)

        counter = 0
        for item in sorted(names):
            counter = counter + 1
            menu[counter] = item

        if len(menu) > 0:

            print "\n\n"
            print '#########################################'
            print '## S3 Buckets                          ##'
            print '#########################################'
            for key in sorted(menu):
                print(str(key) + ":" + menu[key])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    bucket_name = menu[int(ans)]
                    break

        response = client.get_bucket_acl(
            Bucket=bucket_name
        )

        if 'Owner' in response:
            response.pop("ResponseMetadata", None)
            print(pretty(response))
        else:
            print("\n")
            print("############")
            print('No ACL')
            print("############")

    else:
        print("\n")
        print("##################")
        print('No S3 Buckets')
        print("##################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
