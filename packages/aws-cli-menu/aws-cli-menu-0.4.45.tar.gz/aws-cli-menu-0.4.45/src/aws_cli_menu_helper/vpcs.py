
import re
import boto3.session
from .pretty import *

DEBUG =0


def get_vpc_id():
    pattern = r'^vpc\-[a-z0-9]{8}\s*$'
    while True:

        vpc_id = raw_input("Enter vpc id[ENTER]:")
        if re.match(pattern,vpc_id) is not None:


                break

    return vpc_id

def get_vpc_info(session,id):
    client = session.client('ec2')

    response = client.describe_vpcs(VpcIds=[id])
    stacks = response.get('Vpcs')
    return stacks[0]


def get_vpc_tags(session,id):
    client = session.client('ec2')
    response = client.describe_vpcs(VpcIds=[id])
    stacks = response.get('Vpcs')[0]
    tags = stacks.get('Tags')

    return tags

def are_there_vpc_tags(session,id):

    client = session.client('ec2')

    response = client.describe_vpcs(
        DryRun=False,
        VpcIds=[id]
    )

    if 'Vpcs' in response:

        stacks = response['Vpcs']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'][0])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return [False]









def select_vpc_id(session):
    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:

            list=[]

            if 'Tags' in s:
                name = 'Tag: '+str(s['Tags'][0]['Value'])
            else:
                name = 'Tag: None - '+str(s.get('VpcId'))
            vpcid = s.get('VpcId')
            cidr_block = s.get('CidrBlock')

            list.append(name)
            list.append(vpcid)
            list.append(cidr_block)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item]

        if len(menu) >0:

            print "\n\n"
            print '#########################################'
            print '## Select VPC                          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]+' - '+menu[key][1] + ' - '+menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER]")
                if re.match(pattern,ans) is not None:
                    if int(ans) in menu:
                        break


            print"\n\n"

            return menu[int(ans)][1]

def create_vpc_tag(session,id):

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


def delete_vpc_tags(session,id, key, value, dryrun):
    client = session.client('ec2')
    response = client.delete_tags(
        DryRun=dryrun,
        Resources=[id,],
        Tags=[
            {
                'Key': key,
                'Value': value
            },
        ]
    )

    return response

