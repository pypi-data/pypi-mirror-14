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
            #print(str(cluster_name))


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
                                container_instance_arn = menu[int(ans)][0]
                                break

                    print("\n")
                    print("#################################")
                    print("Detailed Container Instance Info")
                    print("#################################")



                    print(pretty(container_instance_arn))

                    matchObj = re.match( r'(.*)\/(.*)', container_instance_arn, re.M|re.I)

                    if matchObj:
                       print "matchObj.group() : ", matchObj.group()
                       print "matchObj.group(1) : ", matchObj.group(1)
                       container_instance_arn =  matchObj.group(2)
                    else:
                       sys.exit(-1)


                    print('container instance arn: '+str(container_instance_arn))

                    response = CLIENT.list_task_definition_families()

                    print("\n")
                    #print(pretty(response))

                    families = response.get('families')

                    menu = {}
                    fields = {}

                    for s in families:

                        list = []

                        list.append(s)
                        fields[s] = list

                    counter = 0
                    for item in sorted(fields):
                        counter = counter + 1
                        menu[counter] = fields[item]

                    if len(menu) > 0:

                        print "\n"
                        print '#########################################'
                        print '## Families                            ##'
                        print '#########################################'
                        for key in sorted(menu):
                            print str(key) + ":" + menu[key][0]

                        pattern = r'^[0-9]+$'
                        while True:

                            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                            if re.match(pattern, ans) is not None:
                                if int(ans) in menu:
                                    family_name = menu[int(ans)][0]
                                    break

                        print"\n"




                    RESPONSE = CLIENT.list_tasks(
                        cluster=str(cluster_name),
                        #containerInstance=str(container_instance_arn),
                        family='hello-world-task',
                        #desiredStatus='RUNNING'
                        #desiredStatus='RUNNING'|'PENDING'|'STOPPED'
                    )

                    print(pretty(RESPONSE))

                    if 'taskArns' in RESPONSE:
                        STACKS = RESPONSE.get('taskArns')

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
                            print('Select Task')
                            print('#######################')
                            for key in sorted(menu):
                                print(str(key)+" : "+str(menu[key][0]))

                            pattern = r'^[0-9]+$'
                            while True:
                                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                                if re.match(pattern, ans) is not None:
                                    if int(ans) in menu:
                                        task_info = menu[int(ans)][0]
                                        break


                            matchObj = re.match( r'(.*)\/(.*)', task_info, re.M|re.I)

                            if matchObj:

                                task = matchObj.group(2)

                                print('task is: '+str(task))

                                response = CLIENT.describe_tasks(
                                    cluster=str(cluster_name),
                                    tasks=[
                                        str(task)
                                    ]
                                )


                                print("\n")
                                print(pretty(response))

                        else:
                            print("\n")
                            print("###############################")
                            print("There Are No Tasks")
                            print("###############################")

                    else:
                        print("\n")
                        print("###############################")
                        print("There Are No Tasks")
                        print("###############################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
