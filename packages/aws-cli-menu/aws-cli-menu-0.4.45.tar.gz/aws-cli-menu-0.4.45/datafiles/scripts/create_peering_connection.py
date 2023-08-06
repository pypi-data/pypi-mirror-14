#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    print("\n")
    print("###############################")
    print('Enter peering connection name')
    print("###############################")
    # Get tag name

    pattern = r'^[0-9a-zA-Z_]+$'
    while True:
        tag_name = raw_input("Enter Tag key name [ENTER]:")
        if re.match(pattern, tag_name) is not None:
            tag_name_ans = tag_name
            break
        else:
            print('Must only contain letters, numbers and underscores with no spaces')

    # Get local vpc to peer
    vpc_id = select_vpc_id(session)
    print('vpc_id is: ' + str(vpc_id))

    # Get whether within this account or to an external account
    account_type_list = ['Internal', 'External']
    account_type = {}

    counter = 0
    for d in sorted(account_type_list):
        counter = counter + 1
        account_type[counter] = d

    print("\n")
    print("###########################################################")
    print("Select whether connection is external to this AWS account.")
    print("###########################################################")
    for key in sorted(account_type):
        print str(key) + ":" + account_type[key]

    while True:
        ans = raw_input("Select account type [ENTER]:")

        if int(ans) in account_type:
            acct_type_ans = account_type[int(ans)]
            break
        else:
            print('Select one of the options above')

    print('account_type: ' + str(acct_type_ans))

    if acct_type_ans == 'Internal':

        # Get vpc if to another account
        client = session.client('ec2')
        response = client.describe_vpcs()
        stacks = response.get('Vpcs')

        menu = {}
        fields = {}

        if len(stacks) > 0:

            for s in stacks:
                list=[]

                if 'Tags' in s:
                    name = s.get('Tags')[0]['Value']
                else:
                    name = 'None listed - '+str(s.get('VpcId'))
                vpcid = s.get('VpcId')

                # Skip the original vpc
                if vpcid == vpc_id:
                    continue

                cidr_block = s.get('CidrBlock')

                list.append(name)
                list.append(vpcid)
                list.append(cidr_block)
                fields[name] = list

            counter = 0
            for item in sorted(fields):
                counter = counter +1
                menu[counter] = fields[item]

            if len(menu) >0:

                print "\n"
                print '#########################################'
                print '## Select VPC                          ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key)+":" + menu[key][0]+' - '+menu[key][1] + ' - '+menu[key][2]

                pattern = r'^[0-9]+$'
                while True:

                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern,ans) is not None:
                        if int(ans) in menu:
                            second_vpc_id = menu[int(ans)][1]
                            break


        client = session.client('ec2')

        menu = get_iam_users(session)

        if len(menu) > 0:
            user_name = menu[1][0]

            account_id = get_account_id(session, user_name)

            matchObj = re.match(
                r'arn:aws:iam::(\d+):user/.*',
                account_id,
                re.M | re.I)

            if matchObj:
                acct_id = matchObj.group(1)

                response = client.create_vpc_peering_connection(
                    DryRun=False,
                    VpcId=vpc_id,
                    PeerVpcId=second_vpc_id,
                    PeerOwnerId=acct_id
                )

                print("\n")
                print(pretty(response))

            else:
                print("\n")
                print("###############################")
                print "Count not find account id!!"
                print("###############################")

        else:
            print("\n")
            print("####################")
            print('No users found')
            print("#####################")

    else:

        # Get account id if to another account

        second_profile_name = get_profile_name()

        # Get vpc if to another account
        second_session = boto3.session.Session(
            profile_name=second_profile_name)
        second_vpc_id = select_vpc_id(second_session)
        print('second_vpc_id is: ' + str(second_vpc_id))

        dryrun_list = ['True', 'False']
        dryrun = {}

        counter = 0
        for d in sorted(dryrun_list):
            counter = counter + 1
            dryrun[counter] = d

        print("\n")
        print("#####################################")
        print("Select Whether a Dryrun or Not")
        print("#####################################")
        for key in sorted(dryrun):
            print str(key) + ":" + dryrun[key]

        while True:

            ans = raw_input("Is this a dry run? [ENTER]:")
            if int(ans) in dryrun:
                if (int(ans) == 1):
                    dryrun_ans = False
                    break
                else:
                    dryrun_ans = True
                    break

        client = session.client('ec2')
        response = client.create_vpc_peering_connection(
            DryRun=dryrun_ans,
            VpcId=vpc_id,
            PeerVpcId=second_vpc_id,
            PeerOwnerId=profile_name
        )

        print("\n")
        print(response)

except (KeyboardInterrupt, SystemExit):
    sys.exit()
