#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")


    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')
    response = client.describe_vpcs()


    if 'Vpcs' in response:

        stacks = response.get('Vpcs')

        if len(stacks) > 0:


            menu = {}
            counter = 0
            for s in stacks:
                counter+=1
                my_list = []

                if 'Tags' in s:
                    name = 'Tag: '+str(s['Tags'][0]['Value'])
                else:
                    name = 'Tag: None - ' + str(s.get('VpcId'))
                vpcid = s.get('VpcId')
                cidr_block = s.get('CidrBlock')

                my_list.append(name)
                my_list.append(vpcid)
                my_list.append(cidr_block)
                my_list.append(s)
                menu[counter] = my_list


            if len(menu) > 0:

                print "\n"
                print '#########################################'
                print '## Select VPC                          ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

                pattern = r'^[0-9]+$'
                while True:

                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            vpc_id = menu[int(ans)][1]
                            info = menu[int(ans)][3]
                            break
                        elif int(ans) ==0:
                            sys.exit(1)

                print "\n"
                print '#########################################'
                print '## VPC Details                         ##'
                print '#########################################'
                print(pretty(info))

            else:
                print("\n")
                print("##############################")
                print('No vpc information found')
                print("##############################")

        else:
            print("\n")
            print("##############################")
            print('No vpc information found')
            print("##############################")

    else:
        print("\n")
        print("##############################")
        print('No vpc information found')
        print("##############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
