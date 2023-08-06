#!/usr/bin/env python


import boto3.session
import sys
from aws_cli_menu_helper import *
from os.path import expanduser
import re
from dateutil.parser import *
import datetime
from collections import defaultdict

DEBUG =0

def date2str(dt):
	return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")


def get_all_account_profiles():
        home = expanduser("~")
        cred_file = home+'/.aws/credentials'

        lines = [line.rstrip('\n') for line in open(cred_file)]

        profiles = []
        for line in lines:
                matchObj = re.match( r'^\s*\[(.*)\]\s*$', line, re.M|re.I)
                if matchObj:

                    if matchObj.group(1) <> 'default':
                        profiles.append(matchObj.group(1))

        return profiles

try:

    profile_names = get_all_account_profiles()


    if DEBUG:
        print('profile names: '+str(profile_names))

    volinfo = defaultdict()


    if len(profile_names) >0:
            for p in profile_names:

                print('Getting information for profile name: '+str(p))

                try:
                    session = boto3.session.Session(profile_name=p)

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


                        ct_datetime = parse(date2str(volumes_iterator.create_time))
                        ct_delta = datetime.datetime.now(ct_datetime.tzinfo) - ct_datetime
                        uptime = str(ct_delta.days)

                        #print('uptime: '+str(uptime))

                        if state == 'available' and uptime > 30:

                            # Add instance info to a dictionary
                            volinfo[vol_id] = {
                                    'Environment':p,
                                    'ID': vol_id,
                                    'Size': size,
                                    'State': state,
                                    'Volume Type': volume_type,
                                    'Tags': tags,
                                    'Uptime':uptime
                            }

                except Exception as e:
		            print(e)

            attributes = ['Environment','ID', 'Size', 'State', 'Volume Type','Tags','Uptime']
            print("\n\n")
            print("#############################################################")
            print("Volumes Detached for 30 Days Or More")
            print("#############################################################\n")
            for vol_id, vol in volinfo.items():
                 for key in attributes:
                       print("{0}: {1}".format(key, vol[key]))
                 print("------")


    else:
        print('There are not any profiles')
        sys.exit()

except (KeyboardInterrupt, SystemExit):
    sys.exit()
