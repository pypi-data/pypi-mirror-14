#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)

    menu = {}

    try:
        client = session.client('iam')
        response = client.list_roles()
        stacks = response.get('Roles')


        fields = {}

        for s in stacks:
            list=[]
            name = str(s.get('RoleName'))
            id = str(s.get('RoleId'))
            list.append(name)
            list.append(id)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item][0]

            if fields[item][0] == 'ecs-instance-role':
                print('ecs-instance-role already exists')
                sys.exit()



    except (KeyboardInterrupt, SystemExit):
        sys.exit()


    client = session.client('iam')

    print("\n")
    role_name = 'ecs-instance-role'
    #policy = '{"Version": "2012-10-17","Statement": [{"Action": "sts:AssumeRole","Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"}}]}'
    #policy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": ["ecs:CreateCluster","ecs:DeregisterContainerInstance","ecs:DiscoverPollEndpoint","ecs:Poll","ecs:RegisterContainerInstance","ecs:StartTelemetrySession","ecs:Submit*","ecr:GetAuthorizationToken","ecr:BatchCheckLayerAvailability","ecr:GetDownloadUrlForLayer","ecr:BatchGetImage"],"Resource": "*"}]}'
    policy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"Service": "ec2.amazonaws.com"},"Action": "sts:AssumeRole"}]}'

    response = client.create_role(
         RoleName=role_name,
         AssumeRolePolicyDocument=policy
    )

    print("\n")
    print(pretty(response))

    response = client.create_instance_profile(
        InstanceProfileName='ecs-instance-role',
        Path='/'
    )

    print("\n")
    print(pretty(response))

    response = client.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role'
    )

    print("\n")
    print(pretty(response))


    response = client.add_role_to_instance_profile(
        InstanceProfileName='ecs-instance-role',
        RoleName=role_name
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
