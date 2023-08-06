#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys

try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('s3')
    response = client.list_buckets()
    stacks = response.get('Buckets')

    if len(stacks) > 0:

        menu = {}
        counter = 0
        for s in stacks:
            counter += 1
            menu[counter] = s['Name']

        print "\n\n"
        print '#########################################'
        print '## Select Object                       ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    object_name = menu[int(ans)]
                    break

        response = client.list_objects(
            Bucket=object_name,
        )

        if 'Contents' not in response:
            print("\n")
            print("#####################################")
            print("There are no objects in the bucket.")
            print("#####################################")
        else:

            stacks = response['Contents']
            if len(stacks) > 0:

                menu = {}
                counter = 0

                for i in stacks:
                    counter += 1
                    my_list = []

                    if 'ETag' in i:
                        my_list.append(i['ETag'])
                        my_list.append(i['StorageClass'])
                        my_list.append(i['Key'])

                        menu[counter] = my_list

                if len(menu) > 0:
                    print "\n\n"
                    print '#########################################'
                    print '## Select Object                       ##'
                    print '#########################################'

                    for key in sorted(menu):
                        print str(key) + ":" + menu[key][2]

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern, ans) is not None:
                            if int(ans) in menu:
                                etag = menu[int(ans)][0]
                                name = menu[int(ans)][2]
                                break

                    response = client.generate_presigned_post(
                        Bucket=object_name,
                        Key=etag
                    )

                    print("\n")
                    print("#######################")
                    print("Object URL is:")
                    print("#######################")
                    print(response['url'] + str(name))

                else:
                    print("\n")
                    print("##################################################")
                    print("No files in bucket.  However, there may be other")
                    print("sub-folders but this program does not yet have the")
                    print("functionality to iterate more than one layer deep.")
                    print("##################################################")
    else:
        print("\n")
        print("#########################")
        print('No S3 buckets found')
        print("#########################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
