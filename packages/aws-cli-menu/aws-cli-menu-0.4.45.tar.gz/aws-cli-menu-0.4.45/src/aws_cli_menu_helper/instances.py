
import boto3.session
import re

DEBUG =0


def get_instances(session):

    client = session.client('ec2')
    response = client.describe_instances()

    if (DEBUG):
        print(response)

    stacks = response.get('Reservations')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]

        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:
            name = s.get('Instances')[0]['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        list.append(name)
        list.append(id)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]

    return menu


def print_instance_menu(menu):

    for key in sorted(menu):
        print str(key)+":" + menu[key][0]

    return



def get_instance_info(session,id):
    client = session.client('ec2')

    response = client.describe_instances(InstanceIds=[id])
    stacks = response.get('Reservations')
    return stacks[0]['Instances'][0]


def select_instance_id(session):
    client = session.client('ec2')
    response = client.describe_instances()
    stacks = response.get('Reservations')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list=[]

            if 'Tags' in s['Instances'][0]:
                name = s.get('Instances')[0]['Tags'][0]['Value']
            else:
                name = 'None listed - '+str(s.get('Instances')[0]['InstanceId'])
            instance_id = s.get('Instances')[0]['InstanceId']

            list.append(name)
            list.append(instance_id)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item]

        if len(menu) >0:

            print "\n\n"
            print '#########################################'
            print '## Select Instance                     ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key)+":" + menu[key][0]+' - '+menu[key][1]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER]")
                if re.match(pattern,ans) is not None:
                    if int(ans) in menu:
                        instance_id = menu[int(ans)][1]
                        break

            return instance_id

    else:
        return 0


def get_instance_tags(session,id):
    client = session.client('ec2')
    response = client.describe_instances(InstanceIds=[id])
    stacks = response.get('Reservations')[0]['Instances'][0]
    tags = stacks.get('Tags')

    return tags


def are_there_instance_tags(session,id):
    client = session.client('ec2')

    response = client.describe_instances(
        DryRun=False,
        InstanceIds=[id]
    )

    if 'Reservations' in response:

        if 'Instances' in response['Reservations'][0]:

            stacks = response['Reservations'][0]['Instances']

            if 'Tags' in stacks[0]:
                if len(stacks[0]['Tags'])>0:
                    return [True,stacks[0]['Tags']]
                else:
                    return [False]
            else:
                return [False]
        else:
            return [False]
    else:
        return [False]


def create_instance_tag(session,id):


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


#def select_instance_id(session):
#    client = session.client('ec2')
#    response = client.describe_instances()
#    stacks = response.get('Reservations')[0]['Instances']

#    menu = {}
#    fields = {}

#    if len(stacks) > 0:

#        for s in stacks:
#            list=[]

#            if 'Tags' in s:
#                name = s.get('Tags')[0]['Value']
#                print('tag name is: '+str(name))
#            else:
#                name = 'None listed - '+str(s.get('InstanceId'))
#            instance_id = s.get('InstanceId')

#            list.append(name)
#            list.append(instance_id)
#            fields[name] = list

#        counter = 0
#        for item in sorted(fields):
#            counter = counter +1
#            menu[counter] = fields[item]

#        if len(menu) >0:

#            print "\n\n"
#            print '#########################################'
#            print '## Instances                           ##'
#            print '#########################################'
#            for key in sorted(menu):
#                print str(key)+":" + menu[key][0]+' - '+menu[key][1]

#            pattern = r'^[0-9]+$'
#            while True:

#                ans = raw_input("Make A Choice: [ENTER]")
#                if re.match(pattern,ans) is not None:
#                    if int(ans) in menu:
#                        vpc_id = menu[int(ans)][1]
#                        break


#            print"\n\n"

#            return menu[int(ans)][1]



def delete_instance_tags(session,id, key, value, dryrun):
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