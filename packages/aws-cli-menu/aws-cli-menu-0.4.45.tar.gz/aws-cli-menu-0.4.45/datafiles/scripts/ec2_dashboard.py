#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n")


    session = boto3.session.Session(profile_name=profile_name)

    print("\n")
    print("** Please wait 5-10 seconds while we collect the information. **")

    menu = {
        1:['Running Instances',[0]],
        2:['Dedicated Hosts',[0]],
        3:['Volumes',[0]],
        4:['Key Pairs',[0]],
        5:['Placement Groups',[0]],
        6:['Elastic IPs',[0]],
        7:['Snapshots',[0]],
        8:['Load Balancers',[0]],
        9:['Security Groups',[0]]
    }

    # Get Running Instances
    client = session.client('ec2')
    response = client.describe_instances()

    stacks = response.get('Reservations')

    sub_menu = {}
    counter = 0
    for s in stacks:

        my_list=[]

        id = str(s.get('Instances')[0]['InstanceId'])

        if 'Tags' in s['Instances'][0]:
            name = s.get('Instances')[0]['Tags'][0]['Value']
        else:
            name = 'no tag - '+str(id)

        my_list.append(name)
        my_list.append(s['Instances'][0]['InstanceId'])

        if 'State' in s['Instances'][0]:
            state = s['Instances'][0]['State']['Name']
        else:
            state = 'none'

        if state == 'running':
            counter+=1
            my_list.append(state)
            sub_menu[counter] = my_list


    if len(sub_menu)>0:
        menu[1][1][0] = int(len(sub_menu))
        menu[1][1].append(sub_menu)

    # Get Hosts
    response = client.describe_hosts()

    sub_menu = {}
    if 'Hosts' in response:

        stacks = response['Hosts']

        if len(stacks)>0:
            counter = 0
            for i in stacks:
                counter+=1
                my_list = []
                my_list.append(i['HostId'])
                my_list.append(i['State'])
                my_list.append(i)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[2][1][0] = int(len(sub_menu))
        menu[2][1].append(sub_menu)


    # Get Volumes
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

    sub_menu= {}
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

        sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[3][1][0] = int(len(sub_menu))
        menu[3][1].append(sub_menu)


    # Get Key Pair Info
    client = session.client('ec2')

    response = client.describe_key_pairs()
    sub_menu= {}

    if 'KeyPairs' in response:
        stacks = response.get('KeyPairs')

        if len(stacks) > 0:


            counter=0
            for s in stacks:
                counter+=1
                my_list=[]
                my_list.append(s['KeyName'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[4][1][0] = int(len(sub_menu))
        menu[4][1].append(sub_menu)


    # Get Placement Groups
    client = session.client('ec2')


    response = client.describe_placement_groups(
        DryRun=False
    )

    stacks = response.get('PlacementGroups')
    sub_menu = {}
    if len(stacks)>0:

        menu = {}
        counter=0
        for i in stacks:
            counter+=1
            my_list = []
            my_list.append(i['GroupName'])
            my_list.append(i)
            sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[5][1][0] = int(len(sub_menu))
        menu[5][1].append(sub_menu)


    # Get Elastic IPs

    client = session.client('ec2')
    response = client.describe_addresses()
    elastic_ips = response.get('Addresses')

    sub_menu= {}
    if len(elastic_ips) > 0:


        counter =0
        for e in elastic_ips:
            counter +=1
            my_list = []
            my_list.append(e['AllocationId'])
            my_list.append(e['PublicIp'])
            my_list.append(e)
            sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[6][1][0] = int(len(sub_menu))
        menu[6][1].append(sub_menu)



    # Get Snapshots
    client = session.client('iam')
    response = client.list_users()
    stacks = response.get('Users')

    sub_menu = {}
    iam_menu = {}
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
        iam_menu[counter] = fields[item]


    if len(iam_menu)>0:
        user_name = iam_menu[1][0]

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

            if len(stacks)>0:

                counter =0
                for i in stacks:
                    counter+=1
                    my_list = []
                    my_list.append(i['Description'])
                    my_list.append(i['SnapshotId'])
                    my_list.append(i)
                    sub_menu[counter]=my_list



    if len(sub_menu)>0:
        menu[7][1][0] = int(len(sub_menu))
        menu[7][1].append(sub_menu)


    # Get Load Balancers
    client = session.client('elb')

    response = client.describe_load_balancers()

    sub_menu= {}
    if 'LoadBalancerDescriptions' in response:
        stacks = response.get('LoadBalancerDescriptions')

        if len(stacks) > 0:

            counter =0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['LoadBalancerName'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[8][1][0] = int(len(sub_menu))
        menu[8][1].append(sub_menu)


    # Get Security Groups
    client = session.client('ec2')
    response = client.describe_security_groups()
    stacks = response.get('SecurityGroups')

    sub_menu = {}
    if len(stacks) > 0:

        counter = 0
        for s in stacks:
            counter += 1
            my_list = []
            my_list.append(s['GroupName'])
            my_list.append(s['Description'])
            my_list.append(s)
            sub_menu[counter] = my_list

    if len(sub_menu)>0:
        menu[9][1][0] = int(len(sub_menu))
        menu[9][1].append(sub_menu)



    print("\n")
    print("######################")
    print("EC2 Dashboard")
    print("######################")
    for key in sorted(menu):
        print str(key)+":" + str(menu[key][0]) + ' - '+str(menu[key][1][0])

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                results = menu[int(ans)]
                break

    if len(results[1])>1:
        menu_title = results[0]
        count = results[1][0]
        new_menu = results[1][1]

        if int(ans) == 1:

            print("\n")
            print("#########################")
            print("Select Running Instance")
            print("#########################")
            for key in sorted(new_menu):
                print str(key)+":" + new_menu[key][0]+'- State: '+str(new_menu[key][2])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        instance_id = new_menu[int(ans)][1]
                        break

            client = session.client('ec2')

            response = client.describe_instances(InstanceIds=[instance_id])
            stacks = response.get('Reservations')
            print("\n")
            print("#################################")
            print("Detailed Instance Information")
            print("#################################")
            print(pretty( stacks[0]['Instances'][0]))

        elif int(ans) ==2:

            print("\n")
            print("#######################################")
            print("Select Host")
            print("#######################################")

            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0])+' - '+str(new_menu[key][1])

            while True:

                ans2 = raw_input("Make a selection [ENTER] (Cntrl-C to exit):")
                if int(ans2) in new_menu:
                    info = new_menu[int(ans2)][2]
                    break

            print("#####################")
            print("Detailed Host Info")
            print("#####################")

            print(pretty(info))


        elif int(ans) ==3:

            print "\n"
            print '#########################################'
            print '## Select Volume                       ##'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0]) + ' - ' + str(new_menu[key][1]) + ' - ' + str(new_menu[key][2])+' - '+str(menu[key][3])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][5]
                        break

            print("\n")
            print("###########################")
            print("Volume Details")
            print("###########################")
            print(pretty(item))

        elif int(ans) ==4:

            print "\n"
            print '#########################################'
            print '## Select Key Pair'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern,ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][1]
                        break


            print("\n")
            print('#######################')
            print('Detailed Key Pair Info')
            print('#######################')
            print(pretty(info))

        elif int(ans) ==5:

            print("\n")
            print("##########################")
            print("Select Placement Groups")
            print("##########################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][1]
                        break

            print("\n")
            print("##################################")
            print("Placement Group Information")
            print("##################################")
            print(pretty(info))


        elif int(ans) ==6:

            print("\n")
            print("######################")
            print("Select Elastic IP")
            print("######################")
            for key in sorted(menu):
                print str(key)+":" + str(new_menu[key][0]) + ' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)]
                        break


            print('#########################')
            print('Detailed Elastic IP Info')
            print('#########################')
            print(pretty(info))


        elif int(ans) ==7:

                print("\n")
                print("######################")
                print("Select Snapshot")
                print("######################")
                for key in sorted(new_menu):
                    print str(key)+":" + str(new_menu[key][0]) + ' - '+str(new_menu[key][1])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in new_menu:
                            info = new_menu[int(ans)][2]
                            break

                print("\n")
                print("#######################")
                print("Detailed Snapshot Info")
                print("#######################")
                print(pretty(info))


        elif int(ans) ==8:

            print("\n")
            print("######################")
            print("Select Load Balancer")
            print("######################")
            for key in sorted(new_menu):
                print str(key)+":" + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][1]
                        break

            print("\n")
            print("############################")
            print("Load Balancer Info")
            print("############################")
            print(pretty(info))


        else:


            print "\n"
            print '#########################################'
            print '## Select Security Group               ##'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + new_menu[key][0] + '-' + str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        answer = new_menu[int(ans)][2]
                        break

            print("\n")
            print("######################################")
            print("Detailed Security Group Information")
            print("######################################")

            print(pretty(answer))




except (KeyboardInterrupt, SystemExit):
    sys.exit()
