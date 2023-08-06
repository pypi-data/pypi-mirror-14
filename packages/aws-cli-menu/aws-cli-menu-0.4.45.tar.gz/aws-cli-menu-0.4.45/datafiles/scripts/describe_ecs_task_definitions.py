#!/usr/bin/env python


import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    PROFILE_NAME = get_profile_name()

    SESSION = boto3.session.Session(profile_name=PROFILE_NAME)
    CLIENT = SESSION.client('ecs')



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
                    name = menu[int(ans)][0]
                    break


        print('name: '+str(name))

        response = CLIENT.list_task_definitions(
            familyPrefix=str(name),
            status='ACTIVE'
            #status='ACTIVE'|'INACTIVE',
            #sort='ASC'|'DESC',
            #nextToken='string',
            #maxResults=123
        )

        print("\n")
        print(pretty(response))

        task_def = response['taskDefinitionArns'][0]

        matchObj = re.match( r'(.*)\/(.*)', task_def, re.M|re.I)

        if matchObj:
           #print "matchObj.group(2) : ", matchObj.group(2)

            response = CLIENT.describe_task_definition(
                taskDefinition=matchObj.group(2)
            )

            print("\n")
            print(pretty(response))


        else:
           print "No match!!"


except (KeyboardInterrupt, SystemExit):
    sys.exit()
