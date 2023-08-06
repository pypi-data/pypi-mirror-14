#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')
    response = client.list_policies(
        Scope='Local'
    )

    if 'Policies' in response:
        stacks = response.get('Policies')

        if len(stacks)>0:

            menu = {}
            counter = 0
            for i in stacks:
                counter +=1
                my_list = []
                my_list.append(i['PolicyName'])
                my_list.append(i['Arn'])
                my_list.append(i['PolicyId'])
                menu[counter]=my_list

            print "\n\n"
            print '#########################################'
            print '## Select Policy                       ##'
            print '#########################################'
            for key in sorted(menu):
                print str(key) + ":" + menu[key][0]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    if int(ans) in menu:
                        arn = menu[int(ans)][1]
                        break


            services = {
                'apigateway': {
                    'Not available yet': 1
                },
                'appstream': {
                    'Not available yet': 1
                },
                'autoscaling': {
                    'Not available yet': 1
                },
                'aws-portal': {
                    'Not available yet': 1
                },
                'cloudformation': {
                    'Not available yet': 1
                },
                'cloudfront': {
                    'Not available yet': 1
                },
                'cloudsearch': {
                    'Not available yet': 1
                },
                'cloudtrail': {
                    'Not available yet': 1
                },
                'cloudwatch': {
                    'Not available yet': 1
                },
                'codecommit': {
                    'Not available yet': 1
                },
                'codedeploy': {
                    'Not available yet': 1
                },
                'codepipeline': {
                    'Not available yet': 1
                },
                'cognito-identity': {
                    'Not available yet': 1
                },
                'cognito-sync': {
                    'Not available yet': 1
                },
                'config': {
                    'Not available yet': 1
                },
                'datapipeline': {
                    'Not available yet': 1
                },
                'devicefarm': {
                    'Not available yet': 1
                },
                'directconnect': {
                    'Not available yet': 1
                },
                'ds': {
                    'Not available yet': 1
                },
                'dynamodb': {
                    'Not available yet': 1
                },
                'ec2': {
                    'AcceptVpcPeeringConnection': 1,
                    'ActivateLicense': 1,
                    'AllocateAddress': 1,
                    'AssignPrivateIpAddresses': 1,
                    'AssociateAddress': 1,
                    'AssociateDhcpOptions': 1,
                    'AssociateRouteTable': 1,
                    'AttachClassicLinkVpc': 1,
                    'AttachInternetGateway': 1,
                    'AttachNetworkInterface': 1,
                    'AttachVolume': 1,
                    'AttachVpnGateway': 1,
                    'AuthorizeSecurityGroupEgress': 1,
                    'AuthorizeSecurityGroupIngress': 1,
                    'BundleInstance': 1,
                    'CancelBundleTask': 1,
                    'CancelConversionTask': 1,
                    'CancelExportTask': 1,
                    'CancelImportTask': 1,
                    'CancelReservedInstancesListing': 1,
                    'CancelSpotFleetRequests': 1,
                    'CancelSpotInstanceRequests': 1,
                    'ConfirmProductInstance': 1,
                    'CopyImage': 1,
                    'CopySnapshot': 1,
                    'CreateCustomerGateway': 1,
                    'CreateDhcpOptions': 1,
                    'CreateFlowLogs': 1,
                    'CreateImage': 1,
                    'CreateInstanceExportTask': 1,
                    'CreateInternetGateway': 1,
                    'CreateKeyPair': 1,
                    'CreateNatGateway': 1,
                    'CreateNetworkAcl': 1,
                    'CreateNetworkAclEntry': 1,
                    'CreateNetworkInterface': 1,
                    'CreatePlacementGroup': 1,
                    'CreateReservedInstancesListing': 1,
                    'CreateRoute': 1,
                    'CreateRouteTable': 1,
                    'CreateSecurityGroup': 1,
                    'CreateSnapshot': 1,
                    'CreateSpotDatafeedSubscription': 1,
                    'CreateSubnet': 1,
                    'CreateTags': 1,
                    'CreateVolume': 1,
                    'CreateVpc': 1,
                    'CreateVpcEndpoint': 1,
                    'CreateVpcPeeringConnection': 1,
                    'CreateVpnConnection': 1,
                    'CreateVpnConnectionRoute': 1,
                    'CreateVpnGateway': 1,
                    'DeactivateLicense': 1,
                    'DeleteCustomerGateway': 1,
                    'DeleteDhcpOptions': 1,
                    'DeleteFlowLogs': 1,
                    'DeleteInternetGateway': 1,
                    'DeleteKeyPair': 1,
                    'DeleteNatGateway': 1,
                    'DeleteNetworkAcl': 1,
                    'DeleteNetworkAclEntry': 1,
                    'DeleteNetworkInterface': 1,
                    'DeletePlacementGroup': 1,
                    'DeleteRoute': 1,
                    'DeleteRouteTable': 1,
                    'DeleteSecurityGroup': 1,
                    'DeleteSnapshot': 1,
                    'DeleteSpotDatafeedSubscription': 1,
                    'DeleteSubnet': 1,
                    'DeleteTags': 1,
                    'DeleteVolume': 1,
                    'DeleteVpc': 1,
                    'DeleteVpcEndpoints': 1,
                    'DeleteVpcPeeringConnection': 1,
                    'DeleteVpnConnection': 1,
                    'DeleteVpnConnectionRoute': 1,
                    'DeleteVpnGateway': 1,
                    'DeregisterImage': 1,
                    'DescribeAccountAttributes': 1,
                    'DescribeAddresses': 1,
                    'DescribeAvailabilityZones': 1,
                    'DescribeBundleTasks': 1,
                    'DescribeClassicLinkInstances': 1,
                    'DescribeConversionTasks': 1,
                    'DescribeCustomerGateways': 1,
                    'DescribeDhcpOptions': 1,
                    'DescribeExportTasks': 1,
                    'DescribeFlowLogs': 1,
                    'DescribeImageAttribute': 1,
                    'DescribeImages': 1,
                    'DescribeImportImageTasks': 1,
                    'DescribeImportSnapshotTasks': 1,
                    'DescribeInstanceAttribute': 1,
                    'DescribeInstanceStatus': 1,
                    'DescribeInstances': 1,
                    'DescribeInternetGateways': 1,
                    'DescribeKeyPairs': 1,
                    'DescribeLicenses': 1,
                    'DescribeMovingAddressess': 1,
                    'DescribeNatGateways': 1,
                    'DescribeNetworkAcls': 1,
                    'DescribeNetworkInterfaceAttribute': 1,
                    'DescribeNetworkInterfaces': 1,
                    'DescribePlacementGroups': 1,
                    'DescribePrefixLists': 1,
                    'DescribeRegions': 1,
                    'DescribeReservedInstances': 1,
                    'DescribeReservedInstancesListing': 1,
                    'DescribeReservedInstancesModifications': 1,
                    'DescribeReservedInstancesOfferings': 1,
                    'DescibeRouteTables': 1,
                    'DescribeSecurityGroups': 1,
                    'DescribeSnapshotAttribute': 1,
                    'DescribeSnapshots': 1,
                    'DescribeSpotDatafeedSubscription': 1,
                    'DescribeSpotFleetInstances': 1,
                    'DescribeSpotFleetRequestHistory': 1,
                    'DescribeSpotFleetRequests': 1,
                    'DescribeSpotInstanceRequests': 1,
                    'DescribeSpotPriceHistory': 1,
                    'DescribeSubnets': 1,
                    'DescribeTags': 1,
                    'DescribeVolumeAttribute': 1,
                    'DescribeVolumeStatus': 1,
                    'DescribeVolumes': 1,
                    'DescribeVpcAttribute': 1,
                    'DescribeVpcClassicLink': 1,
                    'DescribeVpcEndpointServices': 1,
                    'DescribeVpcEndpoints': 1,
                    'DescribeVpcPeeringConnections': 1,
                    'DescribeVpcs': 1,
                    'DescribeVpnConnections': 1,
                    'DescribeVpnGateways': 1,
                    'DescribeClassicLinkVpc': 1,
                    'DetachInternetGateway': 1,
                    'DetachNetworkInterface': 1,
                    'DetachVolume': 1,
                    'DetachVpnGateway': 1,
                    'DisableVgwRoutePropagation': 1,
                    'DisableVpcClassicLink': 1,
                    'DisableVpcClassicLink': 1,
                    'DisassociateAddress': 1,
                    'DissassociateRouteTable': 1,
                    'EnableVgwRoutePropagation': 1,
                    'EnableVolumeIO': 1,
                    'EnableVpcClassicLink': 1,
                    'GetConsoleOutput': 1,
                    'GetPasswordData': 1,
                    'ImportImage': 1,
                    'ImportInstance': 1,
                    'ImportKeyPair': 1,
                    'ImportSnapshot': 1,
                    'ImportVolume': 1,
                    'ModifyHosts': 1,
                    'ModifyIdFormat': 1,
                    'ModifyImageAttribute': 1,
                    'ModifyInstanceAttribute': 1,
                    'ModifyInstancePlacement': 1,
                    'ModifyNetworkInterfaceAttribute': 1,
                    'ModifyReservedInstances': 1,
                    'ModifySnapshotAttribute': 1,
                    'ModifySpotFleetRequest': 1,
                    'ModifySubnetAttribute': 1,
                    'ModifyVolumeAttribute': 1,
                    'ModifyVpcAttribute': 1,
                    'ModifyVpcEndpoint': 1,
                    'MonitorInstances': 1,
                    'MoveAddressToVpc': 1,
                    'PurchaseReservedInstancesOffering': 1,
                    'RebootInstances': 1,
                    'RegisterImages': 1,
                    'RejectVpcPeeringConnection': 1,
                    'ReleaseAddress': 1,
                    'ReleaseHosts': 1,
                    'ReplaceNetworkAclAssociation': 1,
                    'ReplaceNetworkAclEntry': 1,
                    'ReplaceRoute': 1,
                    'ReplaceRouteTableAssociation': 1,
                    'ReportInstanceStatus': 1,
                    'RequestSpotFleet': 1,
                    'RequestSpotInstances': 1,
                    'ResetImageAttribute': 1,
                    'ResetInstanceAttribute': 1,
                    'ResetNetworkInterfaceAttribute': 1,
                    'ResetSnapshotAttribute': 1,
                    'RestoreAddressToClassic': 1,
                    'RevokeSecurityGroupEgress': 1,
                    'RevokeSecuirtyGroupIngress': 1,
                    'RunInstances': 1,
                    'StartInstances': 1,
                    'StopInstances': 1
                },
                'elasticbeanstalk': {
                    'Not available yet': 1
                },
                'elasticloadbalancing': {
                    'Not available yet': 1
                },
                'elasticmapreduce': {
                    'Not available yet': 1
                },
                'elastictranscoder': {
                    'Not available yet': 1
                },
                'elasticache': {
                    'Not available yet': 1
                },
                'es': {
                    'Not available yet': 1
                },
                'glacier': {
                    'Not available yet': 1
                },
                'iam': {
                    'Not available yet': 1
                },
                'importexport': {
                    'Not available yet': 1
                },
                'kms': {
                    'Not available yet': 1
                },
                'kinesis': {
                    'Not available yet': 1
                },
                'lambda': {
                    'Not available yet': 1
                },
                'logs': {
                    'Not available yet': 1
                },
                'machinelearning': {
                    'Not available yet': 1
                },
                'aws-marketplace': {
                    'Not available yet': 1
                },
                'aws-marketplace-management': {
                    'Not available yet': 1
                },
                'mobileanalytics': {
                    'Not available yet': 1
                },
                'opsworks': {
                    'Not available yet': 1
                },
                'redshift': {
                    'Not available yet': 1
                },
                'rds': {
                    'Not available yet': 1
                },
                'route53': {
                    'Not available yet': 1
                },
                'sts': {
                    'Not available yet': 1
                },
                'servicecatalog': {
                    'Not available yet': 1
                },
                'ses': {
                    'Not available yet': 1
                },
                'sns': {
                    'Not available yet': 1
                },
                'sqs': {
                    'Not available yet': 1
                },
                's3': {
                    'AbortMultipartUpload': 1,
                    'CreateBucket': 1,
                    'DeleteBucket': 1,
                    'DeleteBucketPolicy': 1,
                    'DeleteBucketWebsite': 1,
                    'DeleteObject': 1,
                    'DeleteObjectVersion': 1,
                    'GetBucketAct': 1,
                    'GetBucketCORS': 1,
                    'GetBucketLocation': 1,
                    'GetBucketLogging': 1,
                    'GetBucketNotification': 1,
                    'GetBucketPolicy': 1,
                    'GetBucketRequestPayment': 1,
                    'GetBucketTagging': 1,
                    'GetBucketVersioning': 1,
                    'GetBucketWebsite': 1,
                    'GetLifecycleConfiguration': 1,
                    'GetObject': 1,
                    'GetOBjectAcl': 1,
                    'GetObjectTorrent': 1,
                    'GetObjectVersion': 1,
                    'GetObjectVersionAcl': 1,
                    'GetObjectVersionTorrent': 1,
                    'ListAllMyBuckets': 1,
                    'ListBucket': 1,
                    'ListBucketMultipartUploads': 1,
                    'ListBucketVersions': 1,
                    'ListMultipartUploadParts': 1,
                    'PutBucketAcl': 1,
                    'PutBucketCORS': 1,
                    'PutBucketLogging': 1,
                    'PutBucketNotification': 1,
                    'PutBucketPolicy': 1,
                    'PutBucketRequestPayment': 1,
                    'PutBucketTagging': 1,
                    'PutBucketVersioning': 1,
                    'PutBucketWebsite': 1,
                    'PutLifecycleConfiguration': 1,
                    'PubObject': 1,
                    'PutObjectAcl': 1,
                    'PubObjectVersionAcl': 1,
                    'ResotreObject': 1
                },
                'swf': {
                    'Not available yet': 1
                },
                'sdb': {
                    'Not available yet': 1
                },
                'storagegateway': {
                    'Not available yet': 1
                },
                'support': {
                    'Not available yet': 1
                },
                'trustedadvisor': {
                    'Not available yet': 1
                },
                'waf': {
                    'Not available yet': 1
                },
                'workspaces': {
                    'Not available yet': 1
                }
            }

            regions = {
                'us-east-1': 1,  # Virginia
                'us-west-1': 1,  # Northern California
                'us-west-2': 1,  # Oregon
                'eu-west-1': 1,  # Ireland
                'eu-central-1': 1,  # Frankfurt
                'ap-southeast-1': 1,  # Singapore
                'ap-southeast-2': 1,  # Tokyo
                'sa-east-1': 1  # Soa Paulo


            }


            client = session.client('iam')


            menu = {}
            counter = 0
            for i in sorted(regions):
                counter += 1
                menu[counter] = i

            print("\n")
            print("###############################################################")
            print("Select Region To Apply Policy To")
            print("###############################################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    #print('matches pattern')
                    if int(ans) in menu:
                        #print('in profiles dictionary')
                        selected_region = menu[int(ans)]
                        break

            menu = {}
            counter = 0
            for i in sorted(services):
                counter += 1
                menu[counter] = i

            print("\n")
            print("###############################################################")
            print("Select Service To Apply Policy To")
            print("###############################################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    #print('matches pattern')
                    if int(ans) in menu:
                        #print('in profiles dictionary')
                        selected_service = menu[int(ans)]
                        break

            menu = {}
            counter = 0
            for i in sorted(services[selected_service]):
                counter += 1
                menu[counter] = i

            print("\n")
            print("###############################################################")
            print("Select Action To Apply Policy To")
            print("###############################################################")
            for key in sorted(menu):
                print str(key) + ":" + menu[key]

            pattern = r'^[0-9]+$'
            while True:

                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if re.match(pattern, ans) is not None:
                    #print('matches pattern')
                    if int(ans) in menu:
                        #print('in profiles dictionary')
                        action = menu[int(ans)]
                        break

            client = session.client('ec2')

            menu = get_iam_users(session)

            if len(menu) > 0:
                # print(menu)
                # Print the menu
                print("\n")
                print("###############################################")
                print("Select User To Apply Policy To")
                print("###############################################")
                print_user_menu(menu)
                ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                print"\n\n"
                user_name = menu[int(ans)][0]

            account_id = get_account_id(session, user_name)

            print("\n")
            print("###############################################################")
            print("Select Whether this Policy is to Allow or Deny Permissions")
            print("###############################################################")

            print("1. Allow")
            print("2. Deny")

            while True:
                effect_ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
                if int(effect_ans) == 1:
                    effect_answer = 'Allow'
                    break
                elif int(effect_ans) == 2:
                    effect_answer = 'Deny'
                    break

            if selected_service == 'ec2':

                client = session.client('iam')


                response = client.create_policy_version(
                    PolicyArn=arn,
                    PolicyDocument='{"Version": "2012-10-17","Statement": [{"Effect":"' +
                    str(effect_answer) +
                    '","Action":["' +
                    str(selected_service) +
                    ':' +
                    str(action) +
                    '"],"Resource":"' +
                    str(account_id) +
                    '"}]}',

                    SetAsDefault=True
                )

                print("\n")
                print(pretty(response))

        else:
            print("\n")
            print("#######################################")
            print("There are no manage policies")
            print("#######################################")

    else:
        print("\n")
        print("#######################################")
        print("There are no manage policies")
        print("#######################################")

except (KeyboardInterrupt, SystemExit):
    sys.exit()
