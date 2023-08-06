#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('ec2')
    response = client.describe_vpcs()
    stacks = response.get('Vpcs')

    menu = {}
    fields = {}

    if len(stacks) > 0:

        for s in stacks:
            list = []

            if 'Tags' in s:
                name = s.get('Tags')[0]['Value']
            else:
                name = 'None listed - ' + str(s.get('VpcId'))
            vpcid = s.get('VpcId')
            vpc_cidr_block = s.get('CidrBlock')

            list.append(name)
            list.append(vpcid)
            list.append(vpc_cidr_block)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter + 1
            menu[counter] = fields[item]

        if len(menu) > 0:

            print "\n"
            print '#########################################'
            print '## Select VPC                          ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0] + ' - ' + menu[key][1] + ' - ' + menu[key][2]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        vpc_id = menu[int(ans)][1]
                        break

            print"\n"


            response = client.describe_subnets()
            stacks = response.get('Subnets')

            counter = 0
            menu = {}
            for s in stacks:

                if s['VpcId'] == vpc_id:
                    counter += 1
                    menu[counter] = s.get('SubnetId')

            if len(menu)>0:
                print "\n"
                print '#########################################'
                print '## Select Subnet                       ##'
                print '#########################################'
                for key in sorted(menu):
                    print str(key)+":" + menu[key]

                pattern = r'^[0-9]+$'
                while True:
                    ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                    if re.match(pattern,ans) is not None:
                        if int(ans) in menu:
                            subnet_id = menu[int(ans)]
                            break

            else:
                print("\n")
                print("#############################################")
                print("There are no subnets - create subnet first.")
                print("#############################################")
                sys.exit(1)

            print("\n")
            print("Getting image information - please wait...")

            response = client.describe_images(
                Filters=[
                    {
                        'Name': 'image-id',
                        'Values': [
                            'ami-67a3a90d',
                        ]
                    }
                ],
            )
            # print(response)

            if 'Images' in response:
                stacks = response.get('Images')

                menu = {}
                counter=0

                for i in stacks:
                    counter+=1
                    my_list = []
                    my_list.append(i['Name'])
                    my_list.append(i['ImageId'])
                    menu[counter]=my_list

                if len(menu)>0:
                    print "\n"
                    print '#########################################'
                    print '## Select Image                        ##'
                    print '#########################################'
                    for key in sorted(menu):
                        print str(key)+":" + menu[key][0]

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern,ans) is not None:
                            if int(ans) in menu:
                                image_id = menu[int(ans)][1]
                                break


                    InstanceType={
                        1:'t1.micro',
                        2:'t2.micro',
                        3:'t2.small',
                        4:'t2.medium',
                        5:'t2.large',
                        6:'m1.small',
                        7:'m1.medium',
                        8:'m1.large',
                        9:'m1.xlarge',
                        10:'m2.xlarge',
                        11:'m2.2xlarge',
                        12:'m2.4xlarge',
                        13:'m3.medium',
                        14:'m3.large',
                        15:'m3.xlarge',
                        16:'m3.2xlarge',
                        17:'m4.large',
                        18:'m4.xlarge',
                        19:'m4.2xlarge',
                        20:'m4.4xlarge',
                        21:'m4.10xlarge',
                        22:'cr1.8xlarge',
                        23:'i2.xlarge',
                        24:'i2.2xlarge',
                        25:'i2.4xlarge',
                        26:'i2.8xlarge',
                        27:'hi1.4xlarge',
                        28:'hs1.8xlarge',
                        29:'c1.medium',
                        30:'c1.xlarge',
                        31:'c3.large',
                        32:'c3.xlarge',
                        33:'c3.2xlarge',
                        34:'c3.4xlarge',
                        35:'c3.8xlarge',
                        36:'c4.large',
                        37:'c4.xlarge',
                        38:'c4.2xlarge',
                        39:'c4.4xlarge',
                        40:'c4.8xlarge',
                        41:'cc1.4xlarge',
                        42:'cc2.8xlarge',
                        43:'g2.2xlarge',
                        44:'cg1.4xlarge',
                        45:'r3.large',
                        46:'r3.xlarge',
                        47:'r3.2xlarge',
                        48:'r3.4xlarge',
                        49:'r3.8xlarge',
                        50:'d2.xlarge',
                        51:'d2.2xlarge',
                        52:'d2.4xlarge',
                        53:'d2.8xlarge'
                    }


                    print "\n"
                    print '#########################################'
                    print '## Select Image Type                   ##'
                    print '#########################################'
                    for key in sorted(InstanceType):
                        print str(key)+":" + InstanceType[key]

                    pattern = r'^[0-9]+$'
                    while True:
                        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                        if re.match(pattern,ans) is not None:
                            if int(ans) in InstanceType:
                                type = InstanceType[int(ans)]
                                break



                    client = session.resource('ec2')
                    response = client.create_instances(
                        DryRun=False,
                        ImageId=image_id,
                        MinCount=1,
                        MaxCount=1,
                        InstanceType=type,
                        SubnetId=subnet_id,
                    )
                    print("\n")
                    print("#########################")
                    print("New Instance ID is:")
                    print("#########################")
                    print(pretty(response))


                else:
                    print("\n")
                    print("##########################")
                    print("There are no images.")
                    print("##########################")

            else:
                print("\n")
                print("#########################")
                print("There are no images.")
                print("#########################")

        else:
            print("\n")
            print("################################################################")
            print('You need to have a vpc created in order to create an instance')
            print("################################################################")
            sys.exit


except (KeyboardInterrupt, SystemExit):
    sys.exit()
