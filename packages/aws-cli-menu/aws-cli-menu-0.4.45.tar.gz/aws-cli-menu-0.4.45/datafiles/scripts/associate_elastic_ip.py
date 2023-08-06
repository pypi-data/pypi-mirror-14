#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('ec2')

    response = client.describe_addresses()

    stacks = response.get('Addresses')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for i in stacks:

            counter += 1
            my_list = []

            my_list.append(i['PublicIp'])
            my_list.append(i['Domain'])
            if 'AllocationId' in i:
                my_list.append(i['AllocationId'])
            else:
                my_list.append('None')

            menu[counter] = my_list

        print "\n"
        print '#########################################'
        print '## Select Elastic IP Type              ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][0]) + ' - Domain: ' + str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    selected_allocation_id = menu[int(ans)][2]
                    public_ip = menu[int(ans)][0]
                    break

        if selected_allocation_id == 'None':
            print("\n")
            print("########################################")
            print("There is no allocation ID for this IP")
            print("########################################")
            sys.exit(1)

        print('associating to ec2 instance')

        print("\n")
        print("##################################")
        print("Select Instance")
        print("##################################")
        menu = get_instances(session)

        if len(menu) > 0:

            print_instance_menu(menu)

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        instance_id = menu[int(ans)][1]
                        break

            print"\n"
            instance_id = menu[int(ans)][1]
            info = get_instance_info(session, instance_id)

            print("\n")
            print("##################################")
            print("Instance Information")
            print("##################################")
            print(pretty(info))

            private_ip = info['PrivateIpAddress']
            instance_id = info['InstanceId']
            network_interfaces = info['NetworkInterfaces']

            if len(network_interfaces) > 0:

                menu = {}
                counter = 0
                for i in network_interfaces:
                    counter += 1
                    print(pretty(i))
                    menu[counter] = i

                print "\n\n"
                print '#########################################'
                print '## Select Network Interface            ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key) + ":" + menu[key]['NetworkInterfaceId'] + ' -  Description: ' + menu[key]['Description']

                pattern = r'^[0-9]+$'
                while True:

                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            network_interface_id = menu[
                                int(ans)]['NetworkInterfaceId']
                            break

                print('private ip: ' + str(private_ip))
                print('instance id: ' + str(instance_id))
                print('network interface id: ' + str(network_interface_id))
                print('allocation id: ' + str(selected_allocation_id))
                print('public ip: ' + str(public_ip))

                response = client.associate_address(
                    DryRun=False,
                    InstanceId=instance_id,
                    # PublicIp=public_ip,
                    AllocationId=selected_allocation_id,
                    NetworkInterfaceId=network_interface_id,
                    PrivateIpAddress=private_ip,
                    AllowReassociation=True
                )

                print("\n")
                print(pretty(response))

            else:
                print("\n")
                print("####################################################")
                print('There are no network interfaces for this instance.')
                print("####################################################")

    else:
        print("\n")
        print("#########################")
        print('No elastic IPs found.')
        print("#########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
