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

    vol_dict = {}

    for volumes_iterator in client.volumes.all():
        my_list=[]
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


        vol_dict[vol_id] = state

    menu = {}

    counter = 0
    for item in sorted(vol_dict):
        counter = counter + 1
        my_list=[]
        my_list.append(item)
        my_list.append(vol_dict[item])

        menu[counter] = my_list

    if len(menu) > 0:
        print "\n\n"
        print '#########################################'
        print '## Volumes                            ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + str(menu[key][0])+' - '+str(menu[key][1])

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    volume_id = menu[int(ans)][0]
                    break

        client = session.client('ec2')
        response = client.delete_volume(
            DryRun=False,
            VolumeId=volume_id
        )

        print("\n")
        print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
