#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    CLIENT = SESSION.client('ecs')
    RESPONSE = CLIENT.list_clusters()


    if 'clusterArns' in RESPONSE:
        STACKS = RESPONSE.get('clusterArns')

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
            print('Clusters')
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

            print"\n\n"
            print(str(cluster_name))



            RESPONSE = CLIENT.list_container_instances(
                cluster=str(cluster_name),
            )

            print(str(RESPONSE))
            if 'containerInstanceArns' in RESPONSE:
                STACKS = RESPONSE.get('containerInstanceArns')

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
                    print('###########################')
                    print('Select Container Instances')
                    print('###########################')
                    for key in sorted(menu):
                        print(str(key)+" : "+str(menu[key][0]))

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                info = menu[int(ans)][1]
                                break

                    print("\n")
                    print("#################################")
                    print("Detailed Container Instance Info")
                    print("#################################")



                    print(pretty(info))


                else:
                    print("\n")
                    print("#################################")
                    print("There Are No Container Instances")
                    print("#################################")

            else:
                print("\n")
                print("#################################")
                print("There Are No Container Instances")
                print("#################################")

    else:
        print("\n")
        print("#################################")
        print("There Are No Clusters")
        print("#################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
