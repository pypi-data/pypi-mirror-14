#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    CLIENT = SESSION.client('ecs')



    cluster_name = raw_input("Enter cluster name: [ENTER]")
    print(pretty(cluster_name))
    response = CLIENT.create_cluster(
        clusterName=str(cluster_name)
    )

    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
