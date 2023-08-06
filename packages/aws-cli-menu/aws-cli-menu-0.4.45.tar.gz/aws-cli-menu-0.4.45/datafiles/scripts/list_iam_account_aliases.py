#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    response = client.list_account_aliases()


    if 'AccountAliases' in response:

        stacks = response.get('AccountAliases')

        counter =0
        if len(stacks)>0:

            print("\n")
            print("#####################")
            print("Account Aliases")
            print("#####################")
            for i in stacks:
                counter+= 1
                print(str(counter)+'. '+str(i))

        else:
            print("\n")
            print("##############")
            print("No Aliases")
            print("##############")
    else:
        print("\n")
        print("######################")
        print("No Aliases")
        print("######################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
