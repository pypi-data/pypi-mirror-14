
import boto3.session
import re
from .pretty import *


def select_network_interface_id(session):

    client = session.client('ec2')

    response = client.describe_network_interfaces()

    if 'NetworkInterfaces' in response:
        stacks = response['NetworkInterfaces']

        menu = {}
        counter = 0
        for i in stacks:

            counter += 1
            my_list = []
            my_list.append(i['PrivateIpAddress'])

            if 'Attachment' in i:
                if 'Status' in i['Attachment']:
                    my_list.append(i['Attachment']['Status'])
                    my_list.append(i['Attachment']['InstanceOwnerId'])
                else:
                    my_list.append('not defined')
                    my_list.append('not defined')
            else:
                my_list.append('not defined')
                my_list.append('not defined')

            my_list.append(i)

            if 'TagSet' in i:
                if len(i['TagSet'])>0:
                    my_list.append(i['TagSet'])
                else:
                    my_list.append('None')

            my_list.append(i['NetworkInterfaceId'])
            menu[counter] = my_list

        if len(menu)>0:
            print "\n\n"
            print '#########################################'
            print '## Select Interface                    ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ": Tags: " + str(menu[key][4])+' - '+str(menu[key][0]) + ' - ' + str(menu[key][1]) + ' - ' + str(menu[key][2])

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER]")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        id = menu[int(ans)][5]
                        break

            return id
        else:
            return 0


    else:
        return 0


def are_there_network_interface_tags(session,id):
    client = session.client('ec2')

    response = client.describe_network_interfaces(
        DryRun=False,
        NetworkInterfaceIds=[id]
    )

    if 'NetworkInterfaces' in response:

        stacks = response['NetworkInterfaces']

        if 'TagSet' in stacks[0]:
            if len(stacks[0]['TagSet'])>0:
                return [True,stacks[0]['TagSet']]
            else:
                return [False]
        else:
            return [False]
    else:
        return False


def create_network_interface_tag(session,id):


    pattern = r'^[0-9a-zA-Z_]+$'
    while True:

        key_name = raw_input("Enter Tag key name [ENTER]:")
        if re.match(pattern,key_name) is not None:
            key_name_ans = key_name
            break

    while True:

        key_value = raw_input("Enter Tag value [ENTER]:")
        if re.match(pattern,key_value) is not None:
            key_value_ans = key_value
            break

    client = session.client('ec2')

    response = client.create_tags(
        DryRun=False,
        Resources = [id],
        Tags = [
            {
                'Key': key_name_ans,
                'Value': key_value_ans
            }
        ]
    )


    return response
