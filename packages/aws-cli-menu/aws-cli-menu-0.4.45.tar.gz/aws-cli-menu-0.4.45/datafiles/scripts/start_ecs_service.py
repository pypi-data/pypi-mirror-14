#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    client = SESSION.client('ecs')

    response = client.list_clusters()


    if 'clusterArns' in response:
        STACKS = response.get('clusterArns')

        if len(STACKS)>0:

            menu = {}

            counter = 0
            for item in STACKS:
                counter += 1

                matchObj = re.match( r'(.*)\/(.*)', item, re.M|re.I)

                if matchObj:
                   menu[counter] =  matchObj.group(2)

            print("\n")
            print('#######################')
            print('Select Cluster')
            print('#######################')
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        cluster_name = menu[int(ans)]
                        break

            response = client.list_services(
                    cluster=str(cluster_name),
            )

            #print(pretty(response))

            if 'serviceArns' in response:
                STACKS = response.get('serviceArns')

                if len(STACKS)>0:

                    menu = {}
                    temp = {}
                    for i in STACKS:
                        my_list = []
                        my_list.append(i)
                        temp[i] = my_list

                    counter = 0
                    for i in sorted(temp):
                        counter +=1
                        menu[counter]=temp[i]

                    print(pretty(menu))
                    print("\n")
                    print('#######################')
                    print('Select Service')
                    print('#######################')
                    for key in sorted(menu):
                        print(str(key)+" : "+str(menu[key][0]))

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                service_name = menu[int(ans)][0]
                                break


                    matchObj = re.match( r'(.*)\/(.*)', service_name, re.M|re.I)

                    if matchObj:
                       service_name =  matchObj.group(2)

                    print('cluster name: '+str(cluster_name))
                    print('service name: '+str(service_name))


                    response = client.update_service(
                        cluster=str(cluster_name),
                        service=str(service_name),
                        desiredCount=1
                    )

                    print("\n")
                    print(pretty(response))



                else:
                    print("\n")
                    print("###############################")
                    print("There Are No Services")
                    print("###############################")

            else:
                print("\n")
                print("###############################")
                print("There Are No Services")
                print("###############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
