#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    print("\n")
    role_name = raw_input("Enter role name: [ENTER]")

    print("\n")
    print("###############################################################")
    print("Select account you want to allow to have access to this role")
    print("###############################################################")

    new_profile_name = get_profile_name()
    new_session = boto3.session.Session(profile_name=new_profile_name)
    menu = get_iam_users(new_session)

    print("\n")
    print("################################")
    print("Select User")
    print("################################")

    for key in sorted(menu):
        print str(key) + ":" + menu[key][0]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                user_name = menu[int(ans)][0]
                break

    account_id = get_account_id(new_session, user_name)
    matchObj = re.match(r'arn:aws:iam::(\d+):user/.*', account_id, re.M | re.I)

    if matchObj:
        acct_id = matchObj.group(1)
        print('account id: ' + str(acct_id))

        policy = '{"Version": "2012-10-17",  "Statement": [{      "Effect": "Allow", "Principal": {"AWS": "arn:aws:iam::' + str(
            acct_id) + ':user/' + str(user_name) + '"}, "Action": "sts:AssumeRole"}  ]}'

        response = client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##############################")
        print('Could not find account id.')
        print("##############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
