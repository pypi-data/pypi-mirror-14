#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n\n")
    session = boto3.session.Session(profile_name=profile_name)
    client = session.resource('dynamodb')

    table_name = raw_input("Enter table name: [ENTER]")

    k_types = {1: 'HASH', 2: 'RANGE'}
    a_types = {1: ['String', 'S'], 2: ['Number', 'N'], 3: ['Binary', 'B']}
    answers = {1: 'Yes', 2: 'No'}

    key_schema = []
    attribute_definitions = []

    pattern = r'^[0-9]+$'
    attribute_counter = 0

    while True:
        attribute_name = raw_input('Enter attribute name: [ENTER]')

        print "\n\n"
        print '#########################################'
        print '## Select Key Type                     ##'
        print '#########################################'
        for key in sorted(k_types):
            print str(key) + ":" + k_types[key]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in k_types:

                    if attribute_counter > 0:
                        key_type = 'RANGE'
                    else:
                        key_type = k_types[int(ans)]

                    attribute_counter += 1

                    break
        print"\n\n"

        print "\n\n"
        print '#########################################'
        print '## Select Attribute Type               ##'
        print '#########################################'
        for key in sorted(a_types):
            print str(key) + ":" + a_types[key][0]

        pattern = r'^[0-9]+$'
        while True:

            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in a_types:
                    attribute_type = a_types[int(ans)][1]
                    break

        print "\n"
        print '#########################################'
        print '## Enter another attribute?            ##'
        print '#########################################'
        for key in sorted(answers):
            print str(key) + ":" + answers[key]

        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        print(ans)
        if re.match(pattern, ans) is not None:
            if int(ans) in answers:
                print('adding info')
                temp_hash = {}
                temp_hash['AttributeName'] = attribute_name
                temp_hash['KeyType'] = key_type
                key_schema.append(temp_hash)

                temp_hash = {}
                temp_hash['AttributeName'] = attribute_name
                temp_hash['AttributeType'] = attribute_type
                attribute_definitions.append(temp_hash)

                if int(ans) == 2:
                    break

    print"\n\n"

    print(attribute_definitions)
    print(key_schema)

    response = client.create_table(
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        TableName=table_name,
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },

        StreamSpecification={
            'StreamEnabled': False
        }
    )

    print("\n")
    print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
