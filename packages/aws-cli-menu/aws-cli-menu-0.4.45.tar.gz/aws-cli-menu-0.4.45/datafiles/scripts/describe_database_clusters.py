#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    response = describe_db_clusters(session)

    stacks = response.get('DBClusters')

    if len(stacks) > 0:

        for s in stacks:
            print("##################")
            print("DB Cluster")
            print("##################")
            print(pretty(s))
    else:
        print("\n")
        print("#####################")
        print("No DB Clusters")
        print("#####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
