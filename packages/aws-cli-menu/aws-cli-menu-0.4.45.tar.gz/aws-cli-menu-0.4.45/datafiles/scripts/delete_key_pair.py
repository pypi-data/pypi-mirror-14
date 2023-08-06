#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_key_pairs()

    if 'KeyPairs' in response:
        stacks = response.get('KeyPairs')

        if len(stacks) > 0:

            menu = {}
            counter = 0
            for s in stacks:
                counter += 1
                menu[counter] = s.get('KeyName')

            print "\n\n"
            print '#########################################'
            print '## Key Pairs                           ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        keypair_name = menu[int(ans)][1]
                        break

            print"\n\n"

            response = client.delete_key_pair(
                DryRun=False,
                KeyName=keypair_name
            )

            print("\n")
            print(pretty(response))

        else:
            print("\n")
            print("##################")
            print('No Key Pairs')
            print("##################")
    else:
        print("\n")
        print("#################")
        print('No Key Pairs')
        print("#################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
