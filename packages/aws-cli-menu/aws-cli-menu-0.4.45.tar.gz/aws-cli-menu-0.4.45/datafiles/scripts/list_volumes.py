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

    menu = {}
    counter =0
    for item in volumes:
        counter+=1
        my_list = []
        if 'tags' in item:

            if item['tags'] == None:
                name = 'Tag: None'
            else:
                name = item['tags'][0]['Value']
                name = 'Tag: '+name
        else:
            name = 'Tag: None'

        my_list.append(name)
        my_list.append(item['vol_id'])
        my_list.append(item['size'])
        my_list.append(item['state'])

        if 'attachments' in item:
            if len(item['attachments']) == 0:
                my_list.append('not_attached')
            else:
                my_list.append('attached')
        else:
            my_list.append('not_attached')
        my_list.append(item)

        menu[counter]=my_list

    if len(menu)>0:
        print "\n"
        print '#########################################'
        print '## Select Volume                       ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][0]) + ' - ' + str(menu[key][1]) + ' - ' + str(menu[key][2])+' - '+str(menu[key][3])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    info = menu[int(ans)][5]
                    break

        print("\n")
        print("###########################")
        print("Volume Details")
        print("###########################")
        print(pretty(item))
    else:
        print("\n")
        print("###########################")
        print("No Volumes")
        print("###########################")



except (KeyboardInterrupt, SystemExit):
    sys.exit()
