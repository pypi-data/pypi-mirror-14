
import re
import boto3.session

DEBUG =0


def get_internet_gateways(session):

    client = session.resource('ec2')

    internet_gateways = []

    for internet_gateways_iterator in client.internet_gateways.all():

        ig = {}

        ig_id = internet_gateways_iterator.id

        ig['ig_id']= ig_id


        tags = internet_gateways_iterator.tags

        if len(tags) >0:
            ig['tags'] = tags
        else:
            ig['tags']= []

        internet_gateways.append(ig)

    return internet_gateways


def select_internet_gateway_id(session):

    client = session.resource('ec2')

    internet_gateways = []

    for internet_gateways_iterator in client.internet_gateways.all():
        ig = {}

        ig_id = internet_gateways_iterator.id

        ig['ig_id'] = ig_id

        tags = internet_gateways_iterator.tags

        if len(tags) > 0:
            ig['tags'] = tags
        else:
            ig['tags'] = ['There are no tags for the vpc']

        internet_gateways.append(ig)

    menu = {}

    counter = 0
    for item in sorted(internet_gateways):
        counter = counter + 1
        menu[counter] = item['ig_id']

    if len(menu) > 0:
        print "\n\n"
        print '#########################################'
        print '## Select Internet Gateway             ##'
        print '#########################################'

        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER]")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    internet_gateway_id = menu[int(ans)]
                    break

        return internet_gateway_id

    else:
        return 0

def are_there_internet_gateway_tags(session,id):
    client = session.client('ec2')

    response = client.describe_internet_gateways(
        DryRun=False,
        InternetGatewayIds=[id]
    )

    if 'InternetGateways' in response:

        stacks = response['InternetGateways']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            return [False]
        else:
            return [False]
    else:
        return False

def create_internet_gateway_tag(session,id):


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
