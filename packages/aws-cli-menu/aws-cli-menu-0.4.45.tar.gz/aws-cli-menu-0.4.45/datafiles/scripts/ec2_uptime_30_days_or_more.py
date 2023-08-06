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

    ec2info = defaultdict()


    if len(profile_names) >0:
            for p in profile_names:

                print('Getting information for profile name: '+str(p))

                try:
                    session = boto3.session.Session(profile_name=p)

                    client = session.resource('ec2')

                    if DEBUG:
                        print('Created session client')


                    # Get information for all running instances
                    running_instances = client.instances.filter(Filters=[{
                        'Name': 'instance-state-name',
                        'Values': ['running']}])

                    if DEBUG:
                        print('Have the information for all running instances:')
                        print(running_instances)

                    for instance in running_instances:
                        for tag in instance.tags:
                            if 'Name'in tag['Key']:
                                name = tag['Value']

                                lt_datetime = parse(date2str(instance.launch_time))
                                lt_delta = datetime.datetime.now(lt_datetime.tzinfo) - lt_datetime
                                uptime = str(lt_delta.days)

                        if int(uptime) >30:


                           if 't2' not in instance.instance_type and 't1' not in instance.instance_type:


                                # Add instance info to a dictionary
                                ec2info[instance.id] = {
                                    'Environment':p,
                                    'Name': name,
                                    'Type': instance.instance_type,
                                    'State': instance.state['Name'],
                                    'Private IP': instance.private_ip_address,
                                    'Public IP': instance.public_ip_address,
                                    'Launch Time': instance.launch_time,
                                    'Uptime':uptime
                                }

                except Exception as e:
		            print(e)

            attributes = ['Environment','Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time','Uptime']
            print("\n\n")
            print("#############################################################")
            print("EC2 Instance Larger Than M3/R3/C3 and Up For More Than 30 Days")
            print("#############################################################\n")
            for instance_id, instance in ec2info.items():

                if DEBUG:
                    print('instance_id: '+str(instance_id))
                    print('instance: '+str(instance))

                for key in attributes:

                    if key == 'Uptime':
                     print("{0}: {1} days".format(key, instance[key]))
                    else:
                     print("{0}: {1}".format(key, instance[key]))
                print("------")


    else:
        print('There are not any profiles')
        sys.exit()

except (KeyboardInterrupt, SystemExit):
    sys.exit()
