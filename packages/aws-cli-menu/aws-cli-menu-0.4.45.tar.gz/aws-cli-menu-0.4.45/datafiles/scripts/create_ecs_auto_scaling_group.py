#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    ag_name = 'ecs-auto-scaling-group'

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('autoscaling')


    response = client.describe_launch_configurations()

    stacks = response.get('LaunchConfigurations')


    if len(stacks)>0:

        menu = {}
        counter = 0

        for s in stacks:
            counter+=1
            my_list=[]
            my_list.append(s['LaunchConfigurationName'])
            my_list.append(s)
            menu[counter]=my_list

        print "\n\n"
        print '###############################'
        print '## Select Launch Configuration'
        print '###############################'
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    launch_config_name = menu[int(ans)][0]
                    break




        session2 = boto3.session.Session(profile_name=profile_name)
        client2 = session2.client('ec2')
        response = client2.describe_vpcs()
        stacks = response.get('Vpcs')

        menu = {}
        fields = {}

        for s in stacks:
            list = []

            vpcid = s.get('VpcId')

            if 'Tags' in s:
                name = 'Tag: '+str(s.get('Tags')[0]['Value'])
            else:
                name = 'Tag: None - ' + str(vpcid)

            cidr_block = s.get('CidrBlock')

            list.append(name)
            list.append(vpcid)
            list.append(cidr_block)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter + 1
            menu[counter] = fields[item]

        if len(menu) > 0:

            print "\n"
            print '#########################################'
            print '## Select VPC                          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        vpc_id = menu[int(ans)][1]
                        break

            print"\n"


            response = client2.describe_subnets()

            if 'Subnets' in response:
                stacks = response.get('Subnets')

                if len(stacks)>0:

                    menu={}
                    counter = 0
                    for s in stacks:

                        if s['VpcId'] == vpc_id:
                            counter += 1
                            my_list = []
                            my_list.append(s['SubnetId'])
                            my_list.append(s)
                            my_list.append(s['CidrBlock'])
                            my_list.append(s['State'])
                            my_list.append(s['DefaultForAz'])
                            menu[counter]=my_list


                    if len(menu)>0:
                        print("\n")
                        print("####################################")
                        print("Select Subnet")
                        print("####################################")

                        for key in sorted(menu):
                            print str(key) + ":" + str(menu[key][0])+' - '+str(menu[key][2])+' - '+str(menu[key][3])

                        while True:

                            ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                            if int(ans2) in menu:
                                subnet_id = menu[int(ans2)][0]
                                info = menu[int(ans2)][1]

                                break



                    else:
                        print("\n")
                        print("#######################")
                        print("No Subnets In This VPC")
                        print("#######################")

                    print('vpc_id:'+str(vpc_id))
                    print('subnet_id: '+str(subnet_id))


                    session3 = boto3.session.Session(profile_name=profile_name)
                    client3 = session3.client('elb')

                    response = client3.describe_load_balancers()

                    if 'LoadBalancerDescriptions' in response:
                        stacks = response.get('LoadBalancerDescriptions')

                        if len(stacks) > 0:

                            menu= {}
                            counter =0
                            for s in stacks:
                                counter+=1
                                my_list = []
                                my_list.append(s['LoadBalancerName'])
                                my_list.append(s)
                                menu[counter]=my_list

                            print("\n")
                            print("######################")
                            print("Select Load Balancer")
                            print("######################")
                            for key in sorted(menu):
                                print str(key)+":" + str(menu[key][0])

                            pattern = r'^[0-9]+$'
                            while True:
                                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                                if re.match(pattern, ans) is not None:
                                    if int(ans) in menu:
                                        lb_name = menu[int(ans)][0]
                                        break


                            print('load balancer name: '+str(lb_name))
                            print('autoscale group name: '+str(ag_name))
                            print('launch config name: '+str(launch_config_name))
                            print('subnet id:'+str(subnet_id))

                            response = client.create_auto_scaling_group(
                                AutoScalingGroupName=str(ag_name),
                                LaunchConfigurationName=str(launch_config_name),
                                #InstanceId='string',
                                MinSize=1,
                                MaxSize=1,
                                DesiredCapacity=1,
                                DefaultCooldown=60,
                                AvailabilityZones=[
                                    'us-east-1a',
                                ],
                                LoadBalancerNames=[
                                    str(lb_name),
                                ],
                                HealthCheckType='EC2',
                                HealthCheckGracePeriod=300,
                            #    PlacementGroup='string',
                                VPCZoneIdentifier=str(subnet_id)
                            #    TerminationPolicies=[
                            #        'string',
                            #    ],
                            #    NewInstancesProtectedFromScaleIn=True|False,
                            #    Tags=[
                            #        {
                            #            'ResourceId': 'string',
                            #            'ResourceType': 'string',
                            #            'Key': 'string',
                            #            'Value': 'string',
                            #            'PropagateAtLaunch': True|False
                            #        },
                            #    ]
                            )

                            print("\n")
                            print(pretty(response))





                        else:
                            print("\n")
                            print("#####################")
                            print('No Load Balancers')
                            print("#####################")
                    else:
                        print("#####################")
                        print('No Load Balancers')
                        print("#####################")



                else:
                    print("\n")
                    print("#######################")
                    print("No Subnets In This VPC")
                    print("#######################")


            else:
                print("\n")
                print("#######################")
                print("No Subnets In This VPC")
                print("#######################")
        else:
            print("\n")
            print("############################")
            print('No vpc information found')
            print("############################")



except (KeyboardInterrupt, SystemExit):
    sys.exit()
