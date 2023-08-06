
import boto3.session
import re
from .pretty import *


def select_dhcp_option_id(session):

    client = session.client('ec2')
    response = client.describe_dhcp_options(
        DryRun=False
    )

    if 'DhcpOptions' in response:

        stacks = response['DhcpOptions']

        menu = {}
        counter =0
        for i in stacks:
            counter +=1


            my_list = []
            my_list.append(i['DhcpOptionsId'])
            config = i['DhcpConfigurations']

            for c in config:
                if 'domain-name' in c['Key']:
                    my_list.append(c['Values'][0]['Value'])

            menu[counter]=my_list



        print '#########################################'
        print '## Select DHCP Option                  ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER]")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    dhcp_id = menu[int(ans)][0]
                    break


        return dhcp_id

    else:
        return 0

def are_there_dhcp_options_tags(session,id):
    client = session.client('ec2')

    response = client.describe_dhcp_options(
        DryRun=False,
        DhcpOptionsIds=[id]
    )

    #print(pretty(response))

    if 'DhcpOptions' in response:

        stacks = response['DhcpOptions']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return False


def create_dhcp_options_tag(session,id):


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
