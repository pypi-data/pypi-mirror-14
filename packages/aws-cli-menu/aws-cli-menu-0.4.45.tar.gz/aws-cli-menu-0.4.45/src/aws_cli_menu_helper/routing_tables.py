
import boto3.session
from .pretty import *
import re


def select_route_table_id(session):

    client = session.client('ec2')
    response = client.describe_route_tables()
    stacks = response.get('RouteTables')

    menu = {}

    counter = 0
    if len(stacks)>0:
        for s in stacks:
            counter+=1
            list=[]
            name = None

            id = str(s.get('RouteTableId'))

            if 'Tags' in s:

                if len(s['Tags'])>0:

                    tags = s['Tags'][0]
                    name = tags

                else:
                    name = 'no tags - '+str(id)

            vpc_id = str(s.get('VpcId'))
            vpc_name = get_vpc_name(session,vpc_id)

            if name:
                if 'Value' in name:
                    list.append(name['Value'])
                else:
                    list.append(name)
            else:
                list.append(vpc_name)

            list.append(id)
            if 'Associations' in s:

                if len(s['Associations'])>0:
                    if 'RouteTableAssociationId' in s['Associations'][0]:
                        list.append(s['Associations'][0]['RouteTableAssociationId'])

                    else:
                        list.append('none')
                else:
                    list.append('none')
            else:
                list.append('none')

            list.append(s)

            menu[counter] = list

        print "\n\n"
        print '#############################'
        print '## Select Route Table      ##'
        print '#############################'
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][1] + ' - '+str(menu[key][0]))+'- Associaton ID: '+str(menu[key][2])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER]")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    route_table_id = menu[int(ans)][1]
                    info = menu[int(ans)][3]
                    break

        return route_table_id

    else:
        return 0




def get_route_tables(session):

    client = session.client('ec2')
    response = client.describe_route_tables()
    stacks = response.get('RouteTables')

    menu = {}
    fields = {}
    counter=0
    for s in stacks:
        list=[]
        name = None
        id = str(s.get('RouteTableId'))

        if 'Tags' in s:

            if len(s.get('Tags'))>0:
                tags = s.get('Tags')

                if len(tags) > 1:
                    name = tags[0]
            else:
                name = 'no tags - '+str(id)

        vpc_id = str(s.get('VpcId'))
        vpc_name = get_vpc_name(session,vpc_id)

        if name:
            if 'Value' in name:
                list.append(name['Value'])
            else:
                list.append(name)
        else:
            list.append(vpc_name)

        list.append(id)
        if 'Associations' in s:

            if len(s['Associations'])>0:
                if 'RouteTableAssociationId' in s['Associations'][0]:
                    list.append(s['Associations'][0]['RouteTableAssociationId'])
                    list.append(str(s['Associations'][0]['Main']))
                    counter+=1
                else:
                    continue
            else:
                continue
        else:
            continue

        list.append(s)
        menu[counter] = list


    return menu


def print_route_table_menu(menu):
    print "\n"
    print '#############################'
    print '## Select Route Table      ##'
    print '#############################'
    for key in sorted(menu):
        print str(key)+":" + str(menu[key][1] + ' - '+str(menu[key][0]))+'- Main Route Table: '+str(menu[key][3])

    return



def get_route_table_info(session,id):
    client = session.client('ec2')

    response = client.describe_route_tables(RouteTableIds=[id])
    stacks = response.get('RouteTables')
    return stacks


def get_vpc_name(session,id):
    client = session.client('ec2')

    response = client.describe_vpcs(VpcIds=[id])
    stacks = response.get('Vpcs')
    for s in stacks:

        if 'Tags' in s:
            name = s.get('Tags')[0]['Value']
            return name
        else:
            name = 'no tags'
            return name


def create_route_table_tag(session,id):


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


def are_there_route_table_tags(session,id):
    client = session.client('ec2')

    response = client.describe_route_tables(
        DryRun=False,
        RouteTableIds=[id]
    )

    if 'RouteTables' in response:

        stacks = response['RouteTables']

        if 'Tags' in stacks[0]:

            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return False