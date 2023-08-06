
import boto3.session
import re
from .pretty import *

def select_security_group_id(session):



    client = session.client('ec2')
    response = client.describe_security_groups()
    stacks = response.get('SecurityGroups')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for s in stacks:

            counter += 1
            my_list = []
            my_list.append(s['GroupName'])
            my_list.append(s['Description'])
            my_list.append(s)
            my_list.append(s['GroupId'])
            if 'Tags' in s:
                my_list.append(s['Tags'][0]['Key'])
            else:
                my_list.append('no tags')
            menu[counter] = my_list

        print "\n\n"
        print '#########################################'
        print '## Select Security Group               ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])+'-'+str(menu[key][4])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER]")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    sg_id = menu[int(ans)][3]
                    break

        return sg_id

    else:
        return 0


def are_there_security_group_tags(session,id):
    client = session.client('ec2')

    response = client.describe_security_groups(
        DryRun=False,
        GroupIds=[id]
    )

    if 'SecurityGroups' in response:

        stacks = response['SecurityGroups']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return [False]


def create_security_group_tag(session,id):


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


