#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

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
    counter = 0
    for i in volumes:
        counter +=1
        my_list = []
        my_list.append(i['volume_type'])
        my_list.append(i['snapshot_id'])
        my_list.append(i['vol_id'])
        my_list.append(i)

        menu[counter]= my_list

    if len(menu)>0:
        print "\n"
        print '#########################################'
        print '## Select VPC                          ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key][2] + ' - ' + menu[key][0] + ' - ' + menu[key][1]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    volume_id = menu[int(ans)][2]
                    break

        print("\n")
        description = raw_input("Enter a description for the snapshot: [ENTER]")

        response = client.create_snapshot(
            DryRun=False,
            VolumeId=volume_id,
            Description=description
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("##############################")
        print('No snapshots found')
        print("##############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
