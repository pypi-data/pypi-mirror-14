#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('rds')

    response = client.describe_db_instances()

    array = [
        "MasterUsername",
        "MonitoringInterval",
        "LicenseModel",
        "InstanceCreateTime",
        "CopyTagsToSnapshot",
        "OptionGroupMemberships",
        "PendingModifiedValues",
        "Engine",
        "MultiAZ",
        "LatestRestorableTime",
        "AutoMinorVersionUpgrade",
        "PreferredBackupWindow",
        "ReadReplicaDBInstanceIdentifiers",
        "DBName",
        "PreferredMaintenanceWindow",
        "Endpoint",
        "DBInstanceStatus",
        "EngineVersion",
        "AvailabilityZone",
        "StorageType",
        "CACertificateIdentifier",
        "StorageEncrypted",
        "DbInstancePort",
        "DBInstanceIdentifier"
    ]


    if 'DBInstances' in response:
        stacks = response.get('DBInstances')



        if len(stacks) > 0:
            menu = {}
            counter=0
            for s in stacks:
                counter+=1
                my_list = []
                my_list.append(s['DBName'])
                my_list.append(s['DBInstanceIdentifier'])
                my_list.append(s)

                menu[counter]=my_list


            print('#######################')
            print('Select Database')
            print('#######################')
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        info = menu[int(ans)][2]
                        originfo = menu[int(ans)][2]
                        endpoint = menu[int(ans)][2]['Endpoint']
                        id = menu[int(ans)][2]['DbiResourceId']
                        identifier = menu[int(ans)][2]['DBInstanceIdentifier']
                        break


            temp_menu = {}
            for i in info:
                my_list = []
                my_list.append(i)
                my_list.append(info[i])
                if i in array:
                    continue
                temp_menu[i] = my_list

            temp_menu['MasterUserPassword'] = ['MasterUserPassword','xxxxxxx']
            temp_menu['DBPortNumber']= ['DBPortNumber',endpoint['Port']]



            menu = {}
            counter=0
            for i in sorted(temp_menu):
                counter+=1
                my_list = []

                my_list.append(temp_menu[i][0])
                my_list.append(temp_menu[i][1])
                menu[counter]=my_list


            print("\n")
            print("###########################")
            print("Select Feature To Modify")
            print("###########################")
            for key in sorted(menu):
                print str(key)+": " + str(menu[key][0])

            pattern = r'^[0-9]+$'
            while True:
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        name = menu[int(ans)][0]
                        info = menu[int(ans)][1]

                        break


            if name == "AllocatedStorage":

                print("\n")
                print("Current allocated storage size is: "+str(info))
                if originfo['Engine'] == 'mysql':
                    # Valid Values: 5-6144
                    allocated_storage = raw_input("Enter new size.  (Must be between 5-6144GB): [ENTER]")

                elif originfo['Engine'] == 'mariadb':
                    # Valid Values: 5-6144
                    allocated_storage = raw_input("Enter new size.  (Must be between 5-6144GB): [ENTER]")

                elif originfo['Engine'] == 'oracle':
                    #Valid Values: 10-6144
                    allocated_storage = raw_input("Enter new size.  (Must be between 10-6144GB): [ENTER]")


                elif originfo['Engine'] == 'sqlserver':
                    print("######################################")
                    print("Instance can not be modified...sorry.")
                    print("######################################")

                elif  originfo['Engine'] == 'postgresql':
                    # Valid Values: 5-6144
                    allocated_storage = raw_input("Enter new size.  (Must be between 5-6144GB): [ENTER]")


                apply_immediately = yes_or_no('Apply Immediately')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    AllocatedStorage=int(allocated_storage)
                )

                print("\n")
                print(pretty(response))

            elif name == "DBInstanceClass":

                print("\n")
                print("Current DB instance class is: "+str(info))

                instance_class = [
                    'db.t1.micro',
                    'db.m1.small',
                    'db.m1.medium',
                    'db.m1.large',
                    'db.m1.xlarge',
                    'db.m2.xlarge',
                    'db.m2.2xlarge',
                    'db.m2.4xlarge',
                    'db.m3.medium',
                    'db.m3.large',
                    'db.m3.xlarge',
                    'db.m3.2xlarge',
                    'db.m4.large',
                    'db.m4.xlarge',
                    'db.m4.2xlarge',
                    'db.m4.4xlarge',
                    'db.m4.10xlarge',
                    'db.r3.large',
                    'db.r3.xlarge',
                    'db.r3.2xlarge',
                    'db.r3.4xlarge',
                    'db.r3.8xlarge',
                    'db.t2.micro',
                    'db.t2.small',
                    'db.t2.medium',
                    'db.t2.large'
                ]

                menu = {}
                counter=0
                for i in sorted(instance_class):
                    counter+=1
                    menu[counter]=i

                print("\n")
                print("#############################")
                print("Select New DB Instance Class")
                print("#############################")
                for key in sorted(menu):
                    print str(key)+": " + str(menu[key])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            new_class = menu[int(ans)]
                            break

                apply_immediately = yes_or_no('Apply Immediately')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    DBInstanceClass=new_class
                )

                print("\n")
                print(pretty(response))

            elif name == "DBSecurityGroups":
                print("\n")
                print("Current DB security group is: "+str(info))

                client = session.client('rds')

                response = client.describe_db_security_groups()


                if 'DBSecurityGroups' in response:
                    stacks = response.get('DBSecurityGroups')

                    if len(stacks) > 0:
                        menu = {}
                        counter=0
                        for s in stacks:
                            counter+=1
                            my_list = []
                            my_list.append(s['DBSecurityGroupName'])
                            my_list.append(s['DBSecurityGroupDescription'])
                            my_list.append(s)
                            menu[counter]=my_list


                        print('#######################')
                        print('Select Security Group')
                        print('#######################')
                        for key in sorted(menu):
                            print str(key)+": " + str(menu[key][0])+' - '+str(menu[key][1])

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    group_name = menu[int(ans)][0]
                                    break



                        apply_immediately = yes_or_no('Apply Immediately')


                        client = session.client('rds')
                        response = client.modify_db_instance(
                            DBInstanceIdentifier= identifier,
                            ApplyImmediately=apply_immediately,
                            DBSecurityGroups=[group_name]
                        )

                        print("\n")
                        print(pretty(response))


                else:
                    print("\n")
                    print("################################")
                    print("No security groups.")
                    print("Create security group first.")
                    print("################################")

            elif name == "VpcSecurityGroups":
                print("\n")
                print("Current Vpc security group is: "+str(info))

                client = session.client('ec2')
                response = client.describe_security_groups()
                stacks = response.get('SecurityGroups')

                if len(stacks) > 0:

                    menu = {}
                    counter = 0
                    for s in stacks:
                        counter += 1
                        my_list = []
                        my_list.append(s['GroupName'])
                        my_list.append(s['Description'])
                        my_list.append(s)
                        my_list.append(s['VpcId'])
                        menu[counter] = my_list

                    print "\n\n"
                    print '#########################################'
                    print '## Select Security Group               ##'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key) + ":" + menu[key][0] + '-' + str(menu[key][1])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                id = menu[int(ans)][3]
                                break


                    apply_immediately = yes_or_no('Apply Immediately')


                    client = session.client('rds')
                    response = client.modify_db_instance(
                        DBInstanceIdentifier= identifier,
                        ApplyImmediately=apply_immediately,
                        VpcSecurityGroupIds=[id]
                    )

                    print("\n")
                    print(pretty(response))


            elif name == "MasterUserPassword":
                print("\n")
                new_password = raw_input("Enter new master user password: [ENTER]")
                apply_immediately = yes_or_no('Apply Immediately')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    MasterUserPassword=new_password
                )

                print("\n")
                print(pretty(response))

            elif name == "DBParameterGroups":

                print("\n")
                print("Current DB parameters group is: "+str(info))


                client = session.client('rds')

                response = client.describe_db_parameter_groups()


                if 'DBParameterGroups' in response:
                    stacks = response.get('DBParameterGroups')

                    if len(stacks) > 0:
                        menu = {}
                        counter=0
                        for s in stacks:
                            counter+=1
                            my_list = []
                            my_list.append(s['DBParameterGroupName'])
                            my_list.append(s['DBParameterGroupFamily'])
                            my_list.append(s)
                            menu[counter]=my_list


                        print('#######################')
                        print('Select Parameter Group')
                        print('#######################')
                        for key in sorted(menu):
                            print str(key)+": " + str(menu[key][0])+' - '+str(menu[key][1])

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    name = menu[int(ans)][2]
                                    break



                        apply_immediately = yes_or_no('Apply Immediately')



                        client = session.client('rds')
                        response = client.modify_db_instance(
                            DBInstanceIdentifier= identifier,
                            ApplyImmediately=apply_immediately,
                            DBParameterGroupName=name
                        )

                        print("\n")
                        print(pretty(response))


            elif name == "BackupRetentionPeriod":
                print("\n")
                print("Current backup retention period: "+str(info))

                print("\n")
                new_period = raw_input("Enter new retention period: [ENTER]")


                apply_immediately = yes_or_no('Apply Immediately')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    BackupRetentionPeriod=int(new_period)
                )

                print("\n")
                print(pretty(response))

            elif name == "DBPortNumber":
                print("\n")
                print("Current DB port number is: "+str(info))

                if originfo['Engine'] == 'mysql':
                    #Default: 3306
                    #Valid Values: 1150-65535
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535: [ENTER]")

                elif originfo['Engine'] == 'mariadb':
                    # Default: 3306
                    # Valid Values: 1150-65535
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535: [ENTER]")

                elif originfo['Engine'] == 'oracle':
                    # Default: 1521
                    # Valid Values: 1150-65535
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535: [ENTER]")

                elif originfo['Engine'] == 'sqlserver':
                    # Default: 1433
                    # Valid Values: 1150-65535 except for 1434 , 3389 , 47001 , 49152 , and 49152 through 49156 .
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535 but not 1434, 3389, 47001, 49152, and 49152 through 49156: [ENTER]")

                elif  originfo['Engine'] == 'postgresql':
                    # Default: 5432
                    # Valid Values: 1150-65535
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535: [ENTER]")

                elif  originfo['Engine'] == 'aurora':
                    # Default: 3306
                    # Valid Values: 1150-65535
                    print("\n")
                    new_port = raw_input("Enter new port number. Must be betweeen 1150-65535: [ENTER]")

                apply_immediately = yes_or_no('Apply Immediately')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    DBPortNumber=int(new_port)
                )

                print("\n")
                print(pretty(response))

            elif name == "PubliclyAccessible":
                print("\n")
                print("Current publicy accessible value: "+str(info))

                publicly_accessible = yes_or_no('Select Whether Publicly Accessible')


                client = session.client('rds')
                response = client.modify_db_instance(
                    DBInstanceIdentifier= identifier,
                    ApplyImmediately=apply_immediately,
                    PubliclyAccessible=publicly_accessible
                )

                print("\n")
                print(pretty(response))


            else:
                print("\n")
                print("###############")
                print("Error")
                print("###############")

        else:
            print("\n")
            print("####################")
            print('No RDS Instances')
            print("####################")
    else:
        print("\n")
        print("#####################")
        print('No RDS Instances')
        print("#####################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
