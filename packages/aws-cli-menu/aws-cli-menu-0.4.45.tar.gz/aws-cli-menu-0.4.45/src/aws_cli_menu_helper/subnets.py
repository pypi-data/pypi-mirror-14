
import boto3.session
import re
from .pretty import *



def get_subnets(session):

    client = session.client('ec2')
    response = client.describe_subnets()
    stacks = response.get('Subnets')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]

        id = str(s.get('SubnetId'))

        vpc_id = s.get('VpcId')

        vpc_name = get_vpc_name(session,vpc_id)

        cidr_block = s.get('CidrBlock')

        list.append(vpc_name)
        list.append(id)
        list.append(cidr_block)
        fields[cidr_block] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]

    return menu


def print_subnet_menu(menu):

    print "\n\n"
    print '#########################################'
    print '## Select Subnet                      ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key)+":" + menu[key][0]+' - '+str(menu[key][1])+' - '+str(menu[key][2])

    return



def get_subnet_info(session,id):
    client = session.client('ec2')

    response = client.describe_subnets(SubnetIds=[id])
    stacks = response.get('Subnets')
    return stacks



def delete_subnet(session,id,dryrun):
    client = session.client('ec2')

    response = client.delete_subnet(DryRun=dryrun,SubnetId=id)
    return response



def get_vpc_name(session,id):
    client = session.client('ec2')

    response = client.describe_vpcs(VpcIds=[id])
    stacks = response.get('Vpcs')
    for s in stacks:
        if 'Tags' in s:
            name = 'Tag: '+str(s.get('Tags')[0]['Value'])
        else:
            name= 'Tag: None - '+ str(s.get('SubnetId'))
        return name



def get_subnets_for_vpc(session,vpc_id):

    client = session.client('ec2')

    response = client.describe_subnets()
    stacks = response.get('Subnets')

    counter = 0
    for s in stacks:

        if s['VpcId'] == vpc_id:
            counter += 1
            print('######################################')
            print('Subnet #'+str(counter))
            print('######################################')
            print(pretty(s))


def select_subnet_id(session):
    client = session.client('ec2')
    response = client.describe_subnets()
    stacks = response.get('Subnets')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list=[]

            if 'Tags' in s:
                name = 'Tag: '+str(s.get('Tags')[0]['Value'])
            else:
                name= 'Tag: None - '+ str(s.get('SubnetId'))

            subnet_id = s.get('SubnetId')

            list.append(name)
            list.append(subnet_id)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item]

        if len(menu) >0:

            print "\n\n"
            print '#########################################'
            print '## Select Subnet                       ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]+' - '+menu[key][1]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER]")
                if re.match(pattern,ans) is not None:
                    if int(ans) in menu:
                        vpc_id = menu[int(ans)][1]
                        break

            print"\n\n"

            return menu[int(ans)][1]



def get_subnet_tags(session,id):
    client = session.client('ec2')
    response = client.describe_subnets(SubnetIds=[id])
    stacks = response.get('Subnets')[0]
    tags = stacks.get('Tags')

    return tags

def are_there_subnet_tags(session,id):

    client = session.client('ec2')

    response = client.describe_subnets(
        DryRun=False,
        SubnetIds=[id]
    )

    if 'Subnets' in response:

        stacks = response['Subnets']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return [False]






def create_subnet_tag(session,id):


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

def delete_subnet_tags(session,id, key, value, dryrun):
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


def get_subnets_menu_for_vpc(session,vpc_id):

    client = session.client('ec2')

    response = client.describe_subnets()
    stacks = response.get('Subnets')

    counter = 0
    menu = {}
    for s in stacks:

        if s['VpcId'] == vpc_id:
            counter += 1
            menu[counter] = s.get('SubnetId')
            #print(s)

    print "\n\n"
    print '#########################################'
    print '## Select Subnet                       ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key)+":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:

        ans = raw_input("Make A Choice: [ENTER]")
        if re.match(pattern,ans) is not None:
            if int(ans) in menu:
                subnet_id = menu[int(ans)]
                break

    print"\n\n"
    return subnet_id