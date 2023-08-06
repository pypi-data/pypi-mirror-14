#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    client = SESSION.client('ecs')


    print("\n")
    service_name = raw_input("Enter service name: [ENTER]")
    print("\n")
    desired_count = int(raw_input("Enter desired count: [ENTER]"))

    response = client.list_clusters()


    if 'clusterArns' in response:
        STACKS = response.get('clusterArns')

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
            print('Select Cluster')
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




            response = client.list_task_definition_families()

            print("\n")
            #print(pretty(response))

            families = response.get('families')

            menu = {}
            fields = {}

            for s in families:

                list = []

                list.append(s)
                fields[s] = list

            counter = 0
            for item in sorted(fields):
                counter = counter + 1
                menu[counter] = fields[item]

            if len(menu) > 0:

                print "\n"
                print '#########################################'
                print '## Select Task Family                  ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key) + ":" + menu[key][0]

                pattern = r'^[0-9]+$'
                while True:

                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            task_family = menu[int(ans)][0]
                            break


                print('task_family: '+str(task_family))

                response = client.list_task_definitions(
                    familyPrefix=str(task_family),
                    status='ACTIVE'
                    #status='ACTIVE'|'INACTIVE',
                    #sort='ASC'|'DESC',
                    #nextToken='string',
                    #maxResults=123
                )

                print("\n")
                print(pretty(response))

                task_def = response['taskDefinitionArns'][0]

                matchObj = re.match( r'(.*)\/(.*)', task_def, re.M|re.I)

                if matchObj:
                   #print "matchObj.group(2) : ", matchObj.group(2)

                    response = client.describe_task_definition(
                        taskDefinition=matchObj.group(2)
                    )

                    print("\n")
                    print(pretty(response))

                    task_arn = response['taskDefinition']['taskDefinitionArn']
                    container = response['taskDefinition']['containerDefinitions'][0]
                    print('container: ')
                    print(pretty(container))
                    container_name = container['name']
                    port_mappings = container['portMappings']
                    print('port mappings:')
                    print(pretty(port_mappings))
                    container_port = port_mappings[0]['containerPort']


                    print('container port: '+str(container_port))
                    print('container name: '+str(container_name))

                    session2 = boto3.session.Session(profile_name=PROFILE_NAME)

                    client2 = session2.client('elb')

                    response = client2.describe_load_balancers()

                    if 'LoadBalancerDescriptions' in response:
                        stacks = response.get('LoadBalancerDescriptions')

                        if len(stacks) > 0:

                            menu = {}
                            counter = 0
                            for s in stacks:
                                counter += 1
                                menu[counter] = s.get('LoadBalancerName')

                            print "\n"
                            print '#########################################'
                            print '## Select Load Balancer to Delete      ##'
                            print '#########################################'
                            for key in sorted(menu):
                                print str(key) + ":" + menu[key]

                            pattern = r'^[0-9]+$'

                            while True:
                                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                                if re.match(pattern, ans) is not None:
                                    if int(ans) in menu:
                                        elb_name = menu[int(ans)]
                                        break



                            response = client.create_service(
                                cluster=str(cluster_name),
                                serviceName=str(service_name),
                                taskDefinition=str(task_arn),
                                loadBalancers=[
                                    {
                                        'loadBalancerName': str(elb_name),
                                        'containerName': str(container_name),
                                        'containerPort': int(container_port)
                                    },
                                ],
                                desiredCount=desired_count,
                            ##    clientToken='string',
                                role='ecs-service-role'
                            ##    deploymentConfiguration={
                            ##        'maximumPercent': 123,
                            ##        'minimumHealthyPercent': 123
                            ##    }
                            )

                            print("\n")
                            print(pretty(response))

                else:
                   print "No match!!"


except (KeyboardInterrupt, SystemExit):
    sys.exit()
