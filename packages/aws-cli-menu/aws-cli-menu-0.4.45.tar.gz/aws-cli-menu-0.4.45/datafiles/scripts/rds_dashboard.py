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
        1:['DB Instances',[0]],
        2:['Reserved DB Purchases',[0]],
        3:['Snapshots',[0]],
        4:['Manual Snapshots',[0]],
        5:['Automated Snapshots',[0]],
        6:['Recent Events',[0]],
        7:['Event Subscriptions',[0]],
        8:['DB Security Groups',[0]],
        9:['Parameter Groups',[0]],
        10: ['Options Groups',[0]],
        11: ['Subnet Groups',[0]]
    }

    # Get DB Instances
    client = session.client('rds')
    response = client.describe_db_instances()

    sub_menu={}
    if 'DBInstances' in response:
        stacks = response.get('DBInstances')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBName'])
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[1][1][0] = int(len(sub_menu))
        menu[1][1].append(sub_menu)


    # Get Reserved DB Instances
    client = session.client('rds')
    response = client.describe_reserved_db_instances()

    sub_menu={}
    if 'ReservedDBInstances' in response:
        stacks = response.get('ReservedDBInstances')

        if len(stacks) > 0:

            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['ProductDescription'])
                my_list.append(s['ReservedDBInstanceId'])
                my_list.append(s)
                sub_menu[counter]=my_list


    if len(sub_menu)>0:
        menu[2][1][0] = int(len(sub_menu))
        menu[2][1].append(sub_menu)


    # Get RDS Snapshots
    client = session.client('rds')

    response = client.describe_db_snapshots()
    sub_menu={}
    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:
            counter = 0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s['DBSnapshotIdentifier'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[3][1][0] = int(len(sub_menu))
        menu[3][1].append(sub_menu)


    # Get Manual Snapshots
    client = session.client('rds')

    response = client.describe_db_snapshots(
        SnapshotType='manual'
    )

    sub_menu = {}
    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:
            counter = 0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s['DBSnapshotIdentifier'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[4][1][0] = int(len(sub_menu))
        menu[4][1].append(sub_menu)


    # Get Automated Snapshots
    client = session.client('rds')

    response = client.describe_db_snapshots(
        SnapshotType='automated'
    )

    sub_menu={}
    if 'DBSnapshots' in response:
        stacks = response.get('DBSnapshots')

        if len(stacks) > 0:
            counter = 0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s['DBSnapshotIdentifier'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[5][1][0] = int(len(sub_menu))
        menu[5][1].append(sub_menu)


    # Get Recent Events
    client = session.client('rds')

    response = client.describe_events()

    sub_menu= {}
    if 'Events' in response:
        stacks = response.get('Events')

        if len(stacks) > 0:

            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['SourceIdentifier'])
                my_list.append(s['Message'])
                my_list.append(s)
                sub_menu[counter]=my_list


    if len(sub_menu)>0:
        menu[6][1][0] = int(len(sub_menu))
        menu[6][1].append(sub_menu)


    # Get Event Subscriptions
    client = session.client('rds')

    response = client.describe_event_subscriptions()

    sub_menu={}
    if 'EventSubscriptionsList' in response:
        stacks = response.get('EventSubscriptionsList')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['SnsTopicArn'])
                my_list.append(s['Status'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[7][1][0] = int(len(sub_menu))
        menu[7][1].append(sub_menu)


    # Get DB Security Groups

    client = session.client('rds')

    response = client.describe_db_security_groups()

    sub_menu= {}
    if 'DBSecurityGroups' in response:
        stacks = response.get('DBSecurityGroups')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBSecurityGroupName'])
                my_list.append(s['DBSecurityGroupDescription'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[8][1][0] = int(len(sub_menu))
        menu[8][1].append(sub_menu)


    # Get RDS Parameter Groups
    client = session.client('rds')

    response = client.describe_db_parameter_groups()

    sub_menu={}
    if 'DBParameterGroups' in response:
        stacks = response.get('DBParameterGroups')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBParameterGroupName'])
                my_list.append(s['DBParameterGroupFamily'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[9][1][0] = int(len(sub_menu))
        menu[9][1].append(sub_menu)


    # Get Option Groups

    client = session.client('rds')

    response = client.describe_option_groups()

    sub_menu={}
    if 'OptionGroupsList' in response:
        stacks = response.get('OptionGroupsList')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['OptionGroupName'])
                my_list.append(s['OptionGroupDescription'])
                my_list.append(s)
                sub_menu[counter]=my_list


    if len(sub_menu)>0:
        menu[10][1][0] = int(len(sub_menu))
        menu[10][1].append(sub_menu)


    # Get Subnet Groups

    client = session.client('rds')

    response = client.describe_db_subnet_groups()

    sub_menu={}
    if 'DBSubnetGroups' in response:
        stacks = response.get('DBSubnetGroups')

        if len(stacks) > 0:
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBSupnetGroupName'])
                my_list.append(s)
                sub_menu[counter]=my_list

    if len(sub_menu)>0:
        menu[11][1][0] = int(len(sub_menu))
        menu[11][1].append(sub_menu)





    print("\n")
    print("######################")
    print("RDS Dashboard")
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
            print('#######################')
            print('Select Database')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("###########################")
            print("Detailed Database Info")
            print("###########################")
            print(pretty(info))

        elif int(ans) ==2:
            print("\n")
            print('#######################')
            print('Select Database')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("###########################")
            print("Detailed Database Info")
            print("###########################")
            print(pretty(info))


        elif int(ans) ==3:

            print "\n"
            print '#########################################'
            print '## Select Snapshot'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + new_menu[key][0] + '-' + str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

                print('#######################')
                print('Detailed Snapshot Info')
                print('#######################')
                print(pretty(info))

        elif int(ans) ==4:


            print "\n"
            print '#########################################'
            print '## Select Snapshot'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + new_menu[key][0] + '-' + str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print('#######################')
            print('Detailed Snapshot Info')
            print('#######################')
            print(pretty(info))

        elif int(ans) ==5:


            print "\n"
            print '#########################################'
            print '## Select Snapshot'
            print '#########################################'
            for key in sorted(new_menu):
                print str(key) + ":" + str(new_menu[key][0]) + '-' + str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print('#######################')
            print('Detailed Snapshot Info')
            print('#######################')
            print(pretty(info))


        elif int(ans) ==6:
            print("\n")
            print('#######################')
            print('Select Event')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("###########################")
            print("Detailed Event Info")
            print("###########################")
            print(pretty(info))


        elif int(ans) ==7:
            print("\n")
            print('#######################')
            print('Select Event Subscription')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("##################################")
            print("Detailed Event Subscription Info")
            print("##################################")
            print(pretty(info))

        elif int(ans) ==8:
            print("\n")
            print('#######################')
            print('Select Security Group')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])+' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Security Group Info")
            print("##############################")
            print(pretty(info))


        elif int(ans) == 9:
            print("\n")
            print('#######################')
            print('Select Parameter Group')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])+' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Parameter Group Info")
            print("##############################")
            print(pretty(info))

        elif int(ans) == 10:
            print("\n")
            print('#######################')
            print('Select Option Group')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])+' - '+str(new_menu[key][1])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Option Group Info")
            print("##############################")
            print(pretty(info))


        else:

            print("\n")
            print('#######################')
            print('Select Subnet Group')
            print('#######################')
            for key in sorted(new_menu):
                print str(key)+": " + str(new_menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in new_menu:
                        info = new_menu[int(ans)][2]
                        break

            print("\n")
            print("##############################")
            print("Detailed Subnet Group Info")
            print("##############################")
            print(pretty(info))



except (KeyboardInterrupt, SystemExit):
    sys.exit()
