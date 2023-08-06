#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import boto.ec2


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

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
        counter +=1
        my_list = []
        my_list.append(item['vol_id'])

        if len(item['attachments'])>0:
            if 'InstanceId' in item['attachments'][0]:
                my_list.append(item['attachments'][0]['InstanceId'])
                my_list.append(item['attachments'][0]['Device'])
                my_list.append(item['tags'])

                if 'tags' in item:

                    if item['tags'] == None:
                        name = 'Tag: None'
                    else:
                        name = item['tags'][0]['Value']
                        name = 'Tag: '+name
                else:
                    name = 'Tag: None'

                my_list.append(name)
                menu[counter]=my_list


    if len(menu)>0:
        print("\n")
        print('#######################')
        print('Select Volume To Detach')
        print('#######################')

        for key in sorted(menu):
            print str(key) + ":" + menu[key][4]+' - '+menu[key][0]+' - '+str(menu[key][3])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    vol_id = menu[int(ans)][0]
                    inst_id = menu[int(ans)][1]
                    dev = menu[int(ans)][2]

                    break


        client = session.client('ec2')
        response = client.detach_volume(
            DryRun=False,
            VolumeId=vol_id,
            InstanceId=inst_id,
            Device=dev,
            Force=True
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("#############################")
        print("No Attached Volumes")
        print("#############################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
