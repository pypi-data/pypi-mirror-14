#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


import sys

try:

    metrics = {
        'AWS/Billing':[
            ['EstimatedCharges',{'Name':'Currency','Value':'USD'}],
        ],
        'AWS/DynamoDB':[
            ['ProvisionedReadCapacityUnits',{ 'Name':'TableName','Value':''}],
            ['ProvisionedWriteCapacityUnits',{'Name':'TableName','Value':''}],
            ['ConsumedReadCapacityUnits',{'Name':'TableName','Value':''}],
            ['ConsumedWriteCapacityUnits',{'Name':'TableName','Value':''}],
            ['ReturnedItemCount',{'Name':'TableName','Value':''}],
            ['SuccessfulRequestLatency',{'Name':'TableName','Value':''}]
        ],
        'AWS/EBS':[
            ['VolumeIdleTime',{'Name':'VolumeId','Value':''}],
            ['VolumeQueueLength',{'Name':'VolumeId','Value':''}],
            ['VolumeReadOps',{'Name':'VolumeId','Value':''}],
            ['VolumeTotalWriteTime',{'Name':'VolumeId','Value':''}],
            ['VolumeWriteBytes',{'Name':'VolumeId','Value':''}],
            ['VolumeWriteOps',{'Name':'VolumeId','Value':''}]
        ],
        'AWS/EC2':[
            ['CPUCreditBalance',{'Name':'InstanceId','Value':''}],
            ['CPUCreditUsage',{'Name':'InstanceId','Value':''}],
            ['CPUUtilization',{'Name':'AutoScalingGroupName','Value':''}],
            ['DiskReadOps',{'Name':'InstanceId','Value':''}],
            ['DiskWriteBytes',{'Name':'InstanceId','Value':''}],
            ['DiskWriteOps',{'Name':'InstanceId','Value':''}],
            ['NetworkIn',{'Name':'InstanceId','Value':''}],  # or AutoScalingGroupName
            ['NetworkOut',{'Name':'InstanceId','Value':''}],
            ['StatusCheckFailed',{'Name':'InstanceId','Value':''}],
            ['StatusCheckFailed_Instance',{'Name':'InstanceId','Value':''}],
            ['StatusCheckFailed_System',{'Name':'InstanceId','Value':''}]
        ],
        'AWS/ELB':[
            ['BackendConnectionErrors',{'Name':'LoadBalancerName','Value':''}],
            ['HTTPCode_ELB_5XX',{'Name':'LoadBalancerName','Value':''}],
            ['HealthyHostCount',{'Name':'LoadBalancerName','Value':''}],
            ['UnHealthyHostCount',{'Name':'LoadBalancerName','Value':''}]
        ],
        'AWS/RDS':[
            ['BinLogDiskUsage',{'Name':'DBInstanceIdentifier','Value':''}],
            ['CPUUtilization',{'Name':'DBInstanceIdentifier','Value':''}],
            ['DatabaseConnections',{'Name':'DBInstanceIdentifier','Value':''}],
            ['DiskQueueDepth',{'Name':'DBInstanceIdentifier','Value':''}],
            ['FreeStorageSpace',{'Name':'DBInstanceIdentifier','Value':''}],
            ['FreeableMemory',{'Name':'DBInstanceIdentifier','Value':''}],
            ['NetworkReceiveThroughput',{'Name':'DBInstanceIdentifier','Value':''}],
            ['NetworkTransmitThroughput',{'Name':'DBInstanceIdentifier','Value':''}],
            ['ReadIOPS',{'Name':'DBInstanceIdentifier','Value':''}],
            ['ReadLetency',{'Name':'DBInstanceIdentifier','Value':''}],
            ['ReadThroughput',{'Name':'DBInstanceIdentifier','Value':''}],
            ['SwapUsage',{'Name':'DBInstanceIdentifier','Value':''}],
            ['TransactionLogsDiskUsage',{'Name':'DBInstanceIdentifier','Value':''}],
            ['WriteIOPS',{'Name':'DBInstanceIdentifier','Value':''}],
            ['WriteLatency',{'Name':'DBInstanceIdentifier','Value':''}],
            ['WriteThroughput',{'Name':'DBInstanceIdentifier','Value':''}]
        ],
        'AWS/S3':[
            ['NumberOfObjects',{'Name':'BucketName','Value':''}],
            ['BucketSizeBytes',{'Name':'BucketName','Value':''}]
        ],
        'AWS/SQS':[
            ['ApproximateNumberOfMessagesDelayed',{'Name':'QueueName','Value':''}],
            ['ApproximateNumberOfMessagesNotVisible',{'Name':'QueueName','Value':''}],
            ['ApproximateNumberOfMessagesVisible',{'Name':'QueueName','Value':''}],
            ['NumberOfEmptyReceives',{'Name':'QueueName','Value':''}],
            ['NumberOfMessagesDeleted',{'Name':'QueueName','Value':''}],
            ['NumberOfMessagesReceived',{'Name':'QueueName','Value':''}],
            ['NumberOfMessagesSent',{'Name':'QueueName','Value':''}],
            ['SentMessageSize',{'Name':'QueueName','Value':''}]
        ]
    }





    comparison_operators = [
        'GreaterThanOrEqualToThreshold',
        'GreaterThanThreshold',
        'LessThanThreshold',
        'LessThanOrEqualToThreshold'
    ]


    evaluation_periods = [
        60,90,120,180,240,300,600
    ]

    periods = [
        ['1 Minute', 60],
        ['5 Minutes', 300],
        ['15 Minutes', 900],
        ['1 Hour', 3600],
        ['6 Hours', 21600],
        ['1 Day', 86400]
    ]

    statistics = [
        'Average',
        'Minimum',
        'Maximum',
        'Sum',
        'Data Samples'
    ]

    unit = [
        'Seconds',
        'Microseconds',
        'Milliseconds',
        'Bytes',
        'Kilobytes',
        'Megabytes',
        'Gigabytes',
        'Terabytes',
        'Bits',
        'Kilobits',
        'Megabits',
        'Gigabits',
        'Terabits',
        'Percent',
        'Count',
        'Bytes/Second',
        'Kilobytes/Second',
        'Megabytes/Second',
        'Gigabytes/Second',
        'Terabytes/Second',
        'Bits/Second',
        'Kilobits/Second',
        'Megabits/Second',
        'Gigabits/Second',
        'Terabits/Second',
        'Count/Second',
        'None'
    ]

    #{
    #xx	u'EvaluationPeriods': 5,
	#    u'AlarmArn': 'arn:aws:cloudwatch:us-east-1:552526261755:alarm:phidata-prod Read Latency',
    #	u'StateUpdatedTimestamp': datetime.datetime(2015, 12, 18, 13, 53, 32, 267000, tzinfo=tzutc()),
    #	u'AlarmConfigurationUpdatedTimestamp': datetime.datetime(2015, 11, 20, 16, 45, 9, 253000, tzinfo=tzutc()),
    #xx	u'ComparisonOperator': 'GreaterThanOrEqualToThreshold',
    #	u'AlarmActions': [
    #		'arn:aws:sns:us-east-1:552526261755:ProdAlarmTopic'
    #	],
    #	u'Namespace': 'AWS/RDS',
    #	u'StateReasonData': '{"version":"1.0","queryDate":"2015-12-18T13:53:32.256+0000","startDate":"2015-12-18T13:48:00.000+0000","statistic":"Average","period":60,"recentDatapoints":[0.04570626400849357,0.04736982742623864,0.027721502590673578,0.03122498888394842,0.01909246309246309],"threshold":0.025}',
    #xx	u'Period': 60,
    #	u'StateValue': 'OK',
    #xx	u'Threshold': 0.025,
    #xx	u'AlarmName': 'phidata-prod Read Latency',
    #xx	u'Dimensions': [
    #		{
    #xx			u'Name': 'DBInstanceIdentifier',
    #xx			u'Value': 'phidata-prod'
    #		}
    #	],
    #xx	u'Statistic': 'Average',
    #	u'StateReason': 'Threshold Crossed: 1 datapoint (0.01909246309246309) was not greater than or equal to the threshold (0.025).',
    #	u'InsufficientDataActions': [
    #	],
    #	u'OKActions': [
    #		'arn:aws:sns:us-east-1:552526261755:ProdAlarmTopic'
    #	],
    #	u'ActionsEnabled': True,
    #xx	u'MetricName': 'ReadLatency'





    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('cloudwatch')

    menu = {}
    counter = 0
    for i in sorted(metrics):
        counter +=1
        menu[counter] = i

    print "\n"
    print '#######################'
    print '## Select Category   ##'
    print '#######################'
    for key in sorted(menu):
        print str(key)+": " + str(menu[key])

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                metrics = metrics[menu[int(ans)]]
                namespace = menu[int(ans)]
                break

    if len(metrics)>0:

        menu = {}
        counter =0
        for i in sorted(metrics):

            counter+=1
            my_list= []
            my_list.append(i[0])
            my_list.append(i[1])
            menu[counter]=i

        print "\n"
        print '###############################'
        print '## Select Metric For Alarm   ##'
        print '###############################'
        for key in sorted(menu):
            print str(key)+": " + str(menu[key][0])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    metric = menu[int(ans)][0]
                    dimensions = menu[int(ans)][1]
                    break



        print("\n")
        alarm_name = raw_input("Enter Alarm Name: [ENTER]")
        print("\n")
        alarm_description = raw_input("Enter Alarm Description: [ENTER]")


        menu = {}
        counter = 0
        for i in sorted(statistics):
            counter+=1
            menu[counter]=i

        print "\n"
        print '###############################'
        print '## Select Statistic          ##'
        print '###############################'
        for key in sorted(menu):
            print str(key)+": " + str(menu[key])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    statistic = menu[int(ans)]
                    break


        dimensions_name = dimensions['Name']

        if dimensions['Name'] == 'Currency':

                dimension_value = 'USD';

        elif dimensions['Name'] == 'TableName' :

            client = session.client('dynamodb')

            response = client.list_tables()
            stacks = response.get('TableNames')

            if len(stacks) > 0:

                menu = {}
                counter=0
                for item in stacks:
                    counter+=1
                    menu[counter] = item


                print "\n"
                print '###############################'
                print '## Select Table              ##'
                print '###############################'
                for key in sorted(menu):
                    print str(key)+": " + str(menu[key])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            dimensions_value = menu[int(ans)]
                            break



        elif dimensions['Name'] == 'VolumeId' :

            client = session.client('ec2')
            response = client.describe_volumes(
                DryRun=False
            )

            stacks = response.get('Volumes')


            if len(stacks)>0:
                menu = {}
                counter=0

                for s in stacks:
                    counter+=1
                    my_list = []

                    my_list.append(s['VolumeId'])
                    my_list.append(s['VolumeType'])
                    my_list.append(s['Encrypted'])
                    my_list.append(s['State'])
                    if 'Tags' in s:
                        if len(s['Tags'])>0:
                            my_list.append(s['Tags'])
                        else:
                            my_list.append('none')
                    else:
                        my_list.append('none')

                    my_list.append(s)

                    menu[counter]=my_list

                print("\n")
                print("######################")
                print("Select Volume")
                print("######################")
                for key in sorted(menu):
                    print str(key)+":" + menu[key][0]+'- '+str(menu[key][1])+' - '+str(menu[key][2])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            dimension_value = menu[int(ans)][0]
                            break



        elif dimensions['Name'] == 'InstanceId' :

            client = session.client('ec2')
            response = client.describe_instances()

            stacks = response.get('Reservations')

            menu = {}
            fields = {}

            for s in stacks:
                list=[]

                id = str(s.get('Instances')[0]['InstanceId'])

                if 'Tags' in s['Instances'][0]:
                    name = s.get('Instances')[0]['Tags'][0]['Value']
                else:
                    name = 'no tag - '+str(id)

                list.append(name)
                list.append(id)

                if 'State' in s['Instances'][0]:
                    state = s['Instances'][0]['State']['Name']
                else:
                    state = 'none'
                list.append(state)

                fields[name] = list

            counter = 0
            for item in sorted(fields):
                counter = counter +1
                menu[counter] = fields[item]


            if len(menu) > 0:

                print("\n")
                print("######################")
                print("Select Instance")
                print("######################")
                for key in sorted(menu):
                    print str(key)+":" + menu[key][0]+'- State: '+str(menu[key][2])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            dimensions_value = menu[int(ans)][1]
                            break



        elif dimensions['Name'] == 'LoadBalancerName':

            client = session.client('elb')

            response = client.describe_load_balancers()

            if 'LoadBalancerDescriptions' in response:
                stacks = response.get('LoadBalancerDescriptions')

                if len(stacks) > 0:

                    menu= {}
                    counter =0
                    for s in stacks:
                        counter+=1
                        my_list = []
                        my_list.append(s['LoadBalancerName'])
                        my_list.append(s)
                        menu[counter]=my_list

                    print("\n")
                    print("######################")
                    print("Select Load Balancer")
                    print("######################")
                    for key in sorted(menu):
                        print str(key)+":" + str(menu[key][0])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                dimensions_value = menu[int(ans)][0]
                                break


        elif dimensions['Name'] == 'DBInstanceIdentifier' :
            client = session.client('rds')

            response = client.describe_db_instances()

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
                                dimensions_value = menu[int(ans)][1]
                                break





        elif dimensions['Name'] == 'BucketName' :
            client = session.client('s3')
            response = client.list_buckets()
            stacks = response.get('Buckets')

            if len(stacks) > 0:
                menu = {}
                counter=0
                for s in stacks:
                    counter+=1
                    my_list = []
                    my_list.append(s['Name'])
                    my_list.append(s)
                    menu[counter]=my_list

                print "\n"
                print '#############################'
                print '## Select S3 Buckets       ##'
                print '#############################'
                for key in sorted(menu):
                    print str(key)+": " + str(menu[key][0])

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern, ans) is not None:
                        if int(ans) in menu:
                            dimensions_value = menu[int(ans)][0]
                            break


        elif dimensions['Name'] == 'QueueName' :

            client = session.client('sqs')

            response = client.list_queues()

            if 'QueueUrls' in response:
                stacks = response.get('QueueUrls')

                if len(stacks) > 0:

                    menu = {}
                    counter=0
                    for s in stacks:
                        counter+=1
                        menu[counter]=s

                    print("\n")
                    print("##########################")
                    print("Select SQS Queues")
                    print("##########################")
                    for key in sorted(menu):
                        print str(key)+":" + str(menu[key])


                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                dimensions_value = menu[int(ans)][0]
                                break


        else:
            print("\n")
            print("#########################")
            print("No dimension name defined")
            print("#########################")


        menu = {}
        counter =0
        for i in sorted(unit):
            counter+=1
            menu[counter]=i

        print("\n")
        print("##########################")
        print("Select Unit")
        print("##########################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    units = menu[int(ans)]
                    break


        menu = {}
        counter=0
        for i in sorted(evaluation_periods):
            counter+=1
            menu[counter]=i


        print("\n")
        print("##########################")
        print("Select Evaluation Period ")
        print("##########################")
        for key in sorted(menu):
            print str(key)

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    evaluation_period = menu[int(ans)]
                    break

        menu = {}
        counter=0
        for i in sorted(periods):
            counter+=1
            my_list=[]
            my_list.append(i[0])
            my_list.append(i[1])

            menu[counter]=my_list

        print("\n")
        print("##########################")
        print("Select Period")
        print("##########################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key][0])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    period = int(menu[int(ans)][1])
                    break

        menu = {}
        counter =0
        for i in sorted(comparison_operators):
            counter+=1
            menu[counter]=i

        print("\n")
        print("##########################")
        print("Select Compairon Operator")
        print("##########################")
        for key in sorted(menu):
            print str(key)+":" + str(menu[key])

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    operator = menu[int(ans)]
                    break

        threshold = raw_input("Enter criteria threshold (example: 10): [ENTER]")
        threshold = int(threshold) + 0.0

        #print(pretty(alarm_name))
        #print(pretty(alarm_description))
        #print(pretty(metric))
        #print(pretty(namespace))
        #print(pretty(statistic))
        #print(pretty(dimensions_name))
        #print(pretty(dimensions_value))
        #print(pretty(units))
        print(pretty(evaluation_period))
        print(pretty(period))
        #print(pretty(threshold))
        #print(pretty(operator))

        client = session.client('cloudwatch')
        response = client.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=alarm_description,
            ActionsEnabled=True,
            MetricName=metric,
            Namespace=namespace,
            Statistic=statistic,
            Dimensions=[
                {
                    'Name': dimensions_name,
                    'Value': dimensions_value
                },
            ],
            Period=period,
            Unit=units,
            EvaluationPeriods=evaluation_period,
            Threshold=threshold,
            ComparisonOperator=operator
        )

        print("\n")
        print(pretty(response))

    else:
        print("\n")
        print("###########################")
        print("No Sub-Categories")
        print("###########################")






except (KeyboardInterrupt, SystemExit):
    sys.exit()
