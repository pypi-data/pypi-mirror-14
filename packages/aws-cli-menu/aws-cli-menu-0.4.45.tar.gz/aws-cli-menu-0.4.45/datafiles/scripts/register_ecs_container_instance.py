#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    CLIENT = SESSION.client('ecs')
    RESPONSE = CLIENT.list_clusters()


    if 'clusterArns' in RESPONSE:
        STACKS = RESPONSE.get('clusterArns')

        if len(STACKS)>0:

            menu = {}

            counter = 0
            for item in STACKS:
                counter += 1

                matchObj = re.match( r'(.*)\/(.*)', item, re.M|re.I)

                if matchObj:
                   menu[counter] =  matchObj.group(2)

            print("\n")
            print('#######################')
            print('Clusters')
            print('#######################')
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        cluster_name = menu[int(ans)]
                        break

            print"\n\n"
            print(str(cluster_name))

    inst_id_doc = raw_input("Enter instanceIdentityDocument.\nGet by 'curl http://169.254.169.254/latest/dynamic/instance-identity/document/'\n[ENTER]")

    id_doc_sig = raw_input("Enter instanceIdentityDocumentSignature.\nGet by 'curl http://169.254.169.254/latest/dynamic/instance-identity/signature/'\n[ENTER]")

    agent_version = raw_input("Enter ECS Agent Version. [ENTER]")
    agent_hash = raw_input("Enter ECS Ageng Git Commit Hash. [ENTER]")
    docker_version = raw_input("Enter Docker Version. [ENTER]")



    #print(pretty(cluster_name))
    #response = CLIENT.create_cluster(
    #    clusterName=str(cluster_name)
    #)

    #print(pretty(response))


    #response = client.register_container_instance(
    #cluster='string',
    #instanceIdentityDocument='string',
    #instanceIdentityDocumentSignature='string',
    #totalResources=[
    #    {
    #        'name': 'string',
    #        'type': 'string',
    #        'doubleValue': 123.0,
    #        'longValue': 123,
    #        'integerValue': 123,
    #        'stringSetValue': [
    #            'string',
    #        ]
    #    },
    #],
    #versionInfo={
    #    'agentVersion': 'string',
    #    'agentHash': 'string',
    #    'dockerVersion': 'string'
    #},
    #containerInstanceArn='string',
    #attributes=[
    #    {
    #        'name': 'string',
    #        'value': 'string'
    #    },
    #]


except (KeyboardInterrupt, SystemExit):
    sys.exit()
