#!/usr/bin/env python

import boto
import boto3
from aws_cli_menu_helper import *
import sys
import botocore.session

try:



    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)


    client = session.client('iam')
    response = client.list_users()
    stacks = response.get('Users')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]
        name = str(s.get('UserName'))
        id = str(s.get('UserId'))
        list.append(name)
        list.append(id)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]


    if len(menu)>0:
        user_name = menu[1][0]

        response = client.get_user(UserName=str(name))
        stacks = response.get('User')
        arn = stacks['Arn']

        matchObj = re.match(r'arn:aws:iam::(\d+):user/.*', arn, re.M | re.I)

        if matchObj:
            acct_id = matchObj.group(1)
        else:
            print('Error getting account id.')
            sys.exit(1)

        client = session.client('ec2')

        response = client.describe_snapshots(
            DryRun=False,
            OwnerIds=[
                acct_id
            ]
            #Filters = [
            #    {
            #        'Name': 'owner-id',
            #        'Values': [
            #            user_id,
            #        ]
            #    }
            #]
        )

        if 'Snapshots' in response:

            stacks = response['Snapshots']

            if len(stacks)>0:

                menu = {}
                counter =0
                for i in stacks:
                    counter+=1
                    my_list = []
                    my_list.append(i['Description'])
                    my_list.append(i['SnapshotId'])
                    my_list.append(i)
                    menu[counter]=my_list


                print("\n")
                print("######################")
                print("Select Snapshot")
                print("######################")
                for key in sorted(menu):
                    print str(key)+":" + str(menu[key][0]) + ' - '+str(menu[key][1])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            info = menu[int(ans)][2]
                            break

                print("\n")
                print("#######################")
                print("Detailed Snapshot Info")
                print("#######################")
                print(pretty(info))


            else:
                print("\n")
                print("########################")
                print("No snapshosts")
                print("########################")
        else:
            print("\n")
            print("########################")
            print("No snapshosts")
            print("########################")
    else:
        print("\n")
        print("########################")
        print("No account id found")
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
