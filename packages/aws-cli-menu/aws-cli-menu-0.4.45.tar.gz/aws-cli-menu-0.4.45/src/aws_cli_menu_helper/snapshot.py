
import boto3.session
import re
from .pretty import *


def select_snapshot_id(session):

    client = session.client('iam')
    response = client.list_users()
    stacks = response.get('Users')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]
        name = str(s.get('UserName'))
        id = str(s.get('UserId'))
        list.append(name)
        list.append(id)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]


    if len(menu)>0:
        user_name = menu[1][0]

        response = client.get_user(UserName=str(name))
        stacks = response.get('User')
        arn = stacks['Arn']

        matchObj = re.match(r'arn:aws:iam::(\d+):user/.*', arn, re.M | re.I)

        if matchObj:
            acct_id = matchObj.group(1)
        else:
            print('Error getting account id.')
            sys.exit(1)

        client = session.client('ec2')

        response = client.describe_snapshots(
            DryRun=False,
            OwnerIds=[
                acct_id
            ]
            #Filters = [
            #    {
            #        'Name': 'owner-id',
            #        'Values': [
            #            user_id,
            #        ]
            #    }
            #]
        )

        if 'Snapshots' in response:

            stacks = response['Snapshots']

            menu = {}
            counter = 0
            for i in stacks:
                counter +=1
                my_list = []
                my_list.append(i['Description'])
                my_list.append(i['SnapshotId'])
                my_list.append(i['VolumeSize'])
                my_list.append(i['State'])
                my_list.append(str(i['StartTime']))
                menu[counter] = my_list

            print "\n\n"
            print '#############################'
            print '## Select Snapshot         ##'
            print '#############################'
            for key in sorted(menu):
                print str(key)+":" + str(menu[key][0] + ' - '+str(menu[key][2]))+'- State: '+str(menu[key][3]+'-'+str(menu[key][4]))

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER]")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        snapshot_id = menu[int(ans)][1]
                        break

            return snapshot_id
        else:
            return 0


    else:
        return 0


def are_there_snapshot_tags(session,id):
    client = session.client('ec2')

    response = client.describe_snapshots(
        DryRun=False,
        SnapshotIds=[id]
    )

    if 'Snapshots' in response:

        stacks = response['Snapshots']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return False


def create_snapshot_tag(session,id):


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
