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

            if fields[item][0] == 'ecs-service-role':
                print('ecs-service-role already exists')
                sys.exit()



    except (KeyboardInterrupt, SystemExit):
        sys.exit()


    client = session.client('iam')

    print("\n")
    role_name = 'ecs-service-role'
    #policy = '{"Version": "2012-10-17","Statement": [{"Effect": "Allow","Action": ["ec2:AuthorizeSecurityGroupIngress","ec2:Describe*","elasticloadbalancing:DeregisterInstancesFromLoadBalancer","elasticloadbalancing:Describe*","elasticloadbalancing:RegisterInstancesWithLoadBalancer"],"Resource": "*"}]}'
    policy = '{"Version": "2008-10-17","Statement": [{"Sid": "","Effect": "Allow","Principal": {"Service": "ecs.amazonaws.com"},"Action": "sts:AssumeRole"}]}'

    response = client.create_role(
         RoleName=role_name,
         AssumeRolePolicyDocument=policy
    )

    print("\n")
    print(pretty(response))

    print("\n")
    print(pretty(response))

    response = client.create_instance_profile(
        InstanceProfileName='ecs-service-role',
        Path='/'
    )



    response = client.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole'
    )

    print("\n")
    print(pretty(response))

    response = client.add_role_to_instance_profile(
        InstanceProfileName='ecs-service-role',
        RoleName=role_name
    )

    print("\n")
    print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
