
import boto3.session
import re
from .pretty import *


#ec2 = boto3.resource('ec2')
#volume = ec2.Volume('id')

def select_volume_id(session):
    client = session.resource('ec2')

    volumes = []

    for volumes_iterator in client.volumes.all():
        vol_dict = {}

        vol_id = volumes_iterator.id
        attachments = volumes_iterator.attachments
        create_time = volumes_iterator.create_time
        encrypted = volumes_iterator.encrypted
        iops = volumes_iterator.iops
        kms_key_id = volumes_iterator.kms_key_id
        size = volumes_iterator.size
        snapshot_id = volumes_iterator.snapshot_id
        state = volumes_iterator.state
        tags = volumes_iterator.tags
        volume_id = volumes_iterator.volume_id
        volume_type = volumes_iterator.volume_type

        vol_dict['vol_id'] = vol_id
        vol_dict['attachments'] = attachments
        vol_dict['create_time'] = create_time
        vol_dict['encrypted'] = encrypted
        vol_dict['iops'] = iops
        vol_dict['kms_key_id'] = kms_key_id
        vol_dict['size'] = size
        vol_dict['snapshot_id'] = snapshot_id
        vol_dict['state'] = state
        vol_dict['tags'] = tags
        vol_dict['volume_type'] = volume_type
        volumes.append(vol_dict)


    menu= {}
    counter = 0
    for item in volumes:
        #print(pretty(item))
        counter +=1
        my_list = []
        my_list.append(item['vol_id'])
        if 'attachments' in item:
            if len(item['attachments'])>0:
                my_list.append(item['attachments'][0]['InstanceId'])
                my_list.append(item['attachments'][0]['Device'])
            else:
                my_list.append('none')
                my_list.append('none')
        else:
            my_list.append('none')
            my_list.append('none')

        my_list.append(item['tags'])
        menu[counter]=my_list

    if len(menu)>0:
        print("\n")
        print('#######################')
        print('Select Volume')
        print('#######################')

        for key in sorted(menu):
            print str(key) + ":" + menu[key][0]+' - '+str(menu[key][3])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER]")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    vol_id = menu[int(ans)][0]
                    inst_id = menu[int(ans)][1]
                    dev = menu[int(ans)][2]
                    break

        return vol_id
    else:
        return 0


def are_there_volume_tags(session,id):
    client = session.client('ec2')

    response = client.describe_volumes(
        DryRun=False,
        VolumeIds=[id]
    )


    if 'Volumes' in response:

        stacks = response['Volumes']

        if 'Tags' in stacks[0]:
            if len(stacks[0]['Tags'])>0:
                return [True,stacks[0]['Tags']]
            else:
                return [False]
        else:
            return [False]
    else:
        return False