#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

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

            print("\n")
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
                        name = menu[int(ans)][0]
                        info = menu[int(ans)][2]
                        break


            if 'IPRanges' in info and 'EC2SecurityGroups' in info and len(info['IPRanges'])>0 and len(info['EC2SecurityGroups'])>0:
                stacks = info['IPRanges']

                if len(stacks)>0:

                    menu = {}
                    counter = 0
                    for i in stacks:
                        counter+=1
                        my_list = []
                        my_list.append(i['CIDRIP'])
                        my_list.append(i)
                        menu[counter]=my_list


                    #'u'IPRanges': [
                	#	{
			        #        u'Status': 'authorizing',
			        #        u'CIDRIP': '192.168.0.0/16'
		            #    }
                    print("\n")
                    print('#######################')
                    print('Select CIDRIP')
                    print('#######################')
                    for key in sorted(menu):
                        print str(key)+": " + str(menu[key][0])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                cidr = menu[int(ans)][0]
                                break

                    stacks = info['EC2SecurityGroups']
                    if len(stacks)>0:


                        menu= {}
                        counter=0
                        for i in stacks:
                            counter+=1
                            my_list=[]
                            my_list.append(i['EC2SecurityGroupName'])
                            my_list.append(i)
                            menu[counter]=my_list

                        print("\n")
                        print('##########################')
                        print('Select EC2 Security Group')
                        print('##########################')
                        for key in sorted(menu):
                            print str(key)+": " + str(menu[key][0])

                        pattern = r'^[0-9]+$'
                        while True:
                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    id = menu[int(ans)][1]['EC2SecurityGroupId']
                                    owner = menu[int(ans)][1]['EC2SecurityGroupOwnerId']
                                    info = menu[int(ans)][1]
                                    break

                        response = client.revoke_db_security_group_ingress(
                            DBSecurityGroupName=name,
                            CIDRIP=cidr,
                            EC2SecurityGroupId=id,
                            EC2SecurityGroupOwnerId=owner
                        )

                        print("\n")
                        print(pretty(response))



                    else:
                        print("\n")
                        print("############################")
                        print("No EC2 Security Groups")
                        print("############################")

                else:
                    print("\n")
                    print("#####################")
                    print("No IPs Provided")
                    print("#####################")



            elif 'IPRanges' in info and len(info['IPRanges'])>0:

                stacks = info['IPRanges']
                if len(stacks)>0:

                    menu = {}
                    counter = 0
                    for i in stacks:
                        counter+=1
                        my_list = []
                        my_list.append(i['CIDRIP'])
                        my_list.append(i)
                        menu[counter]=my_list


                    #'u'IPRanges': [
                	#	{
			        #        u'Status': 'authorizing',
			        #        u'CIDRIP': '192.168.0.0/16'
		            #    }
                    print("\n")
                    print('#######################')
                    print('Select CIDRIP')
                    print('#######################')
                    for key in sorted(menu):
                        print str(key)+": " + str(menu[key][0])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                cidr = menu[int(ans)][0]
                                break



                    response = client.revoke_db_security_group_ingress(
                        DBSecurityGroupName=name,
                        CIDRIP=cidr
                    )

                    print(pretty(response))

                else:
                    print("\n")
                    print("#####################")
                    print("No IPs Provided")
                    print("#####################")

            elif 'EC2SecurityGroups' in info and len(info['EC2SecurityGroups'])>0:

                stacks = info['EC2SecurityGroups']
                if len(stacks)>0:


                    menu= {}
                    counter=0
                    for i in stacks:
                        counter+=1
                        my_list=[]
                        my_list.append(i['EC2SecurityGroupName'])
                        my_list.append(i)
                        menu[counter]=my_list

                    print("\n")
                    print('##########################')
                    print('Select EC2 Security Group')
                    print('##########################')
                    for key in sorted(menu):
                        print str(key)+": " + str(menu[key][0])

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                id = menu[int(ans)][1]['EC2SecurityGroupId']
                                owner = menu[int(ans)][1]['EC2SecurityGroupOwnerId']
                                info = menu[int(ans)][1]
                                break


        	    	#{
	        		#u'Status': 'authorized',
		    	    #u'EC2SecurityGroupName': 'default',
			        #u'EC2SecurityGroupOwnerId': '899486234253',
			        #u'EC2SecurityGroupId': 'sg-7f0f1117'
		            #}

                    response = client.revoke_db_security_group_ingress(
                        DBSecurityGroupName=name,
                        EC2SecurityGroupId=id,
                        EC2SecurityGroupOwnerId=owner
                    )

                    print("\n")
                    print(pretty(response))


                else:
                    print("\n")
                    print("############################")
                    print("No EC2 Security Groups")
                    print("############################")

            else:
                print("\n")
                print("############################")
                print("No EC2 Security Groups")
                print("############################")

        else:
            print("\n")
            print("########################")
            print('No RDS Security Groups')
            print("########################")
    else:
        print("\n")
        print("########################")
        print('No RDS Security Groups')
        print("########################")


except (KeyboardInterrupt, SystemExit):
    sys.exit()
