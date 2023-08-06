#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    # arn:partition:service:region:account-id:resource
    # arn:partition:service:region:account-id:resourcetype/resource
    # arn:partition:service:region:account-id:resourcetype:resource

    services = {
        'autoscaling': {
            'AttachInstances': 1,
            'CompleteLifecycleAction':1,
            'CreateAutoScalingGroup':1
        },
        'cloudformation': {
            'CancelUpdateStack': 1,
            'CreateStack':1,
            'CreateUploadBucket':1
        },
        'cloudfront': {
            'CreateCloudFrontOriginAccessIdentity': 1,
            'CreateDistribution':1,
            'CreateInvalidation':1
        },
        'cloudsearch': {
            'Not available yet': 1
        },
        'cloudtrail': {
            'BuilSuggesters': 1,
            'CreateDomain':1,
            'DefineAnalysisScheme':1
        },
        'cloudwatch': {
            'DeleteAlarms': 1,
            'DescribeAlarmHistory':1,
            'DescribeAlarms':1
        },
        'codecommit': {
            'BatchGetRepositories': 1,
            'CreateBranch':1,
            'CreateRepository':1
        },
        'codedeploy': {
            'AddTagsToOnPremisesInstances': 1,
            'BatchGetApplications':1,
            'BatchGetDeployments':1
        },
        'codepipeline': {
            'AcknowledgeJob': 1,
            'AcknowledgeThirdPartyJob':1,
            'CreateCustomActionType':1
        },
        'cognito-identity': {
            'CreateIdentityPool': 1,
            'DeleteIdentityPool':1,
            'DeleteIdentities':1
        },
        'cognito-sync': {
            'BulkPublish': 1,
            'DeleteDataset':1,
            'DescribeDataset':1
        },
        'config': {
            'DeleteDeliveryChannel': 1,
            'DeliverConfigSnapshot':1,
            'DescribeConfigurationRecorderStatus':1
        },
        'datapipeline': {
            'ActivatePipeline': 1,
            'AddTags':1,
            'CreatePipeline':1
        },
        'devicefarm': {
            'CreateDevicePool': 1,
            'CreateProject':1,
            'CreateUpload':1
        },
        'directconnect': {
            'AllocateConnectionOnInterconnect': 1,
            'AllocatePrivateVirtualInterface':1,
            'AllocatePublicVirtualInterface':1
        },
        'ds': {
            'CreateComputer': 1,
            'CreateDirectory':1,
            'CreateSnapshot':1
        },
        'dynamodb': {
            'BatchGetItem': 1,
            'BatchWriteItem':1,
            'CreateTable':1
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
            'CheckDNSAvailability': 1,
            'CreateApplication':1,
            'CreateApplicationVersion':1
        },
        'elasticloadbalancing': {
            'AddTags': 1,
            'ApplySecurityGroupsToLoadBalancer':1,
            'AttachLoadBalancerToSubnets':1
        },
        'elastictranscoder': {
            'CancelJob': 1,
            'CreateJob':1,
            'CreatePipeline':1
        },
        'elasticache': {
            'AuthorizeCacheSecurityGroupIngress': 1,
            'CopySnapshot':1,
            'CreateCacheCluster':1
        },
        'es': {
            'AddTags': 1,
            'CreateElasticsearchDomain':1,
            'DeleteElasticsearchDomain':1
        },
        'glacier': {
            'AbortVaultLock': 1,
            'AddTagsToVault':1,
            'AbortMultipartUpload':1
        },
        'iam': {
            'AddRoleToInstanceProfile': 1,
            'AddUserToGroup':1,
            'AddClientIDToOpenIDConnectProvider':1
        },
        'importexport': {
            'CreateJob': 1,
            'UpdateJob':1,
            'CancelJob':1
        },
        'kms': {
            'CreateAlias': 1,
            'CreateGrant':1,
            'CreateKey':1
        },
        'kinesis': {
            'AddTagsToStream': 1,
            'CreateStream':1,
            'DecreaseStreamRetentionPeriod':1
        },
        'lambda': {
            'AddPermission': 1,
            'CreateAlias':1,
            'CreateEventSourceMapping':1
        },
        'machinelearning': {
            'CreateBatchPrediction': 1,
            'CreateDataSourceFromRDS':1,
            'CreateDataSourceFromRedshift':1
        },
        'aws-marketplace': {
            'Subscribe': 1,
            'Unsubscribe':1,
            'ViewSubscriptions':1
        },
        'aws-marketplace-management': {
            'uploadFiles': 1,
            'viewMarketing':1,
            'viewReports':1
        },
        'mobileanalytics': {
            'PutEvents': 1,
            'GetReports':1,
            'GetFinancialReports':1
        },
        'opsworks': {
            'AssignVolume': 1,
            'AssociateElasticIp':1,
            'AttachElasticLoadBalancer':1
        },
        'redshift': {
            'AuthorizeClusterSecurityGroupIngress': 1,
            'AuthorizeSnapshotAccess':1,
            'CancelQuerySession':1,
            'CopyClusterSnapshot':1,
            'CreateCluster':1,
            'CreateClusterParameterGroup':1,
            'CreateClusterSecurityGroup':1,
            'CreateClusterSnapshot':1,
            'CreateClusterSubnetGroup':1,
            'CreateEventSubscription':1,
            'CreateHsmClientCertificate':1,
            'CreateHsmConfiguration':1,
            'CreateTags':1,
            'DeleteCluster':1,
            'DeleteClusterParameterGroup':1,
            'DeleteClusterSecurityGroup':1,
            'DeleteClusterSnapshot':1,
            'DeleteClusterSubnetGroup':1,
            'DeleteEventSubscription':1,
            'DeleteHsmClientCertificate':1,
            'DeleteHsmConfiguration':1,
            'DeleteTags':1,
            'DescribeClusterParameterGroups':1,
            'DescribeClusterParameters':1,
            'DescribeClusterSecurityGroups':1,
            'DescribeClusterSnapshots':1,
            'DescribeClusterSubnetGroups':1,
            'DescribeClusterVersions':1,
            'DescribeClusters':1,
            'DescribeDefaultClusterParameters':1,
            'DescribeEventCategories':1,
            'DescribeEvents':1,
            'DescribeHsmClientCertificates':1,
            'DescribeHsmConfigurations':1,
            'DescribeLoggingStatus':1,
            'DescribeOrderableClusterOptions':1,
            'DescribeReservedNodeOfferings':1,
            'DescribeReservedNodes':1,
            'DescribeResize':1,
            'DescribeTags':1,
            'DisableLogging':1,
            'DisableSnapshotCopy':1,
            'EnableLogging':1,
            'EnableSnapshotCopy':1,
            'ModifyCluster':1,
            'ModifyClusterParameterGroup':1,
            'ModifyClusterSubnetGroup':1,
            'ModifyEventSubscription':1,
            'ModifySnapshotCopyRetentionPeriod':1,
            'PurchaseReservedNodeOffering':1,
            'RebootCluster':1,
            'ResetClusterParameterGroup':1,
            'RestoreFromClusterSnapshot':1,
            'RevokeClusterSecurityGroupIngress':1,
            'RevokeSnapshotAccess':1,
            'RotateEncryptionKey':1,
            'RotateEncryptionKey':1,
            'ViewQueriesInConsole':1
        },
        'rds': {
            'AddTagsToResource': 1,
            'AddSourceIdentifierToSubscription':1,
            'ApplyPendingMaintenanceAction':1,
            'AuthorizeDBSecurityGroupIngress':1,
            'CopyDBClusterSnapshot':1,
            'CopyDBParameterGroup':1,
            'CopyDBSnapshot':1,
            'CopyOptionGroup':1,
            'CreateDBClusterParameterGroup':1,
            'CreateDBClusterSnapshot':1,
            'CreateDBCluster':1,
            'CreateDBInstance':1,
            'CreateDBInstanceReadReplica':1,
            'CreateDBParameterGroup':1,
            'CreateDBSecurityGroup':1,
            'CreateDBSnapshot':1,
            'CreateDBSubnetGroup':1,
            'CreateEventSubscription':1,
            'CreateOptionGroup':1,
            'DeleteDBClusterParameterGroup':1,
            'DeleteDBClusterSnapshot':1,
            'DeleteDBCluster':1,
            'DeleteDBInstance':1,
            'DeleteDBParameterGroup':1,
            'DeleteDBSecurityGroup':1,
            'DeleteDBSnapshot':1,
            'DeleteDBSubnetGroup':1,
            'DeleteEventSubscription':1,
            'DeleteOptionGroup':1,
            'DescribeAccountAttributes':1,
            'DescribeCertificate':1,
            'DescribeEngineDefaultClusterParameters':1,
            'DescribeEngineDefaultParameters':1,
            'DescribeDBClusterParameterGroups':1,
            'DescribeDBClusterParameters':1,
            'DescribeDBClusterSnapshots':1,
            'DescribeDBClusters':1,
            'DescribeDBInstances':1,
            'DescribeDBLogFiles':1,
            'DescribeDBParameterGroups':1,
            'DescribeDBParameters':1,
            'DescribeDBSecurityGroups':1,
            'DescribeDBSnapshots':1,
            'DescribeDBEngineVersions':1,
            'DescribeDBSubnetGroups':1,
            'DescribeEventCategories':1,
            'DescribeEvents':1,
            'DescribeEventSubscriptions':1,
            'DescribeOptionGroups':1,
            'DescribeOptionGroupOptions':1,
            'DescribeOrderableDBInstanceOptions':1,
            'DescribePendingMaintenanceActions':1,
            'DescribeReservedDBInstances':1,
            'DescribeReservedDBInstancesOfferings':1,
            'DownloadDBLogFilePortion':1,
            'FailoverDBCluster':1,
            'ListTagsForResource':1,
            'ModifyDBClusterParameterGroup':1,
            'ModifyDBCluster':1,
            'ModifyDBInstance':1,
            'ModifyDBParameterGroup':1,
            'ModifyDBSnapshotAttribute':1,
            'ModifyDBSubnetGroup':1,
            'ModifyEventSubscription':1,
            'ModifyOptionGroup':1,
            'PromoteReadReplica':1,
            'PurchaseReservedDBInstancesOffering':1,
            'RebootDBInstance':1,
            'RemoveSourceIdentifierFromSubscription':1,
            'RemoveTagsFromResource':1,
            'RestoreDBClusterFromSnapshot':1,
            'RestoreDBClusterToPointInTime':1,
            'RestoreDBInstanceFromDBSnapshot':1,
            'RestoreDBInstanceToPointInTime':1,
            'ResetDBClusterParameterGroup':1,
            'ResetDBParameterGroup':1,
            'RevokeDBSecurityGroupIngress':1
        },
        'route53': {
            'AssociateVPCWithHostedZone': 1,
            'ChangeResourceRecordSets':1,
            'ChangeTagsForResource':1,
            'CreateHealthCheck':1,
            'CreateHostedZone':1,
            'CreateReusableDelegationSet':1,
            'DeleteHealthCheck':1,
            'DeleteHostedZone':1,
            'DeleteReusableDelegationSet':1,
            'DisableDomainAutoRenew':1,
            'DisassociateVPCFromHostedZone':1,
            'EnableDomainAutoRenew':1,
            'GetChange':1,
            'GetCheckerIpRanges':1,
            'GetGeoLocation':1,
            'GetHealthCheck':1,
            'GetHealthCheckCount':1,
            'GetHealthCheckLastFailureReason':1,
            'GetHealthCheckStatus':1,
            'GetHostedZone':1,
            'GetHostedZoneCount':1,
            'GetReusableDelegationSet':1,
            'ListGeoLocations':1,
            'ListHealthChecks':1,
            'ListHostedZones':1,
            'ListHostedZonesByName':1,
            'ListResourceRecordSets':1,
            'ListReusableDelegationSets':1,
            'ListTagsForResource':1,
            'ListTagsForResources':1,
            'UpdateHealthCheck':1,
            'UpdateHostedZoneComment':1
        },
        'sts': {
            'AssumeRole': 1,
            'AssumeRoleWithSAML':1,
            'AssumeRoleWithWebIdentity':1,
            'DecodeAuthorizationMessage':1,
            'GetFederationToken':1,
            'GetSessionToken':1
        },
        'ses': {
            'DeleteIdentity': 1,
            'DeleteVerifiedEmailAddress':1,
            'GetIdentityDkimAttributes':1
        },
        'sns': {
            'AddPermission': 1,
            'ConfirmSubscription':1,
            'CreatePlatformApplication':1
        },
        'sqs': {
            'AddPermission': 1,
            'ChangeMessageVisibility':1,
            'ChangeMessageVisibilityBatch':1,
            'CreateQueue':1,
            'DeleteMessage':1,
            'DeleteMessageBatch':1,
            'DeleteQueue':1,
            'GetQueueAttributes':1,
            'GetQueueUrl':1,
            'ListDeadLetterSourceQueues':1,
            'ListQueues':1,
            'PurgeQueue':1,
            'ReceiveMessage':1,
            'RemovePermission':1,
            'SendMessage':1,
            'SendMessageBatch':1,
            'SetQueueAttributes':1
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
            'CancelTimer': 1,
            'CancelWorkflowExecution':1,
            'CompleteWorkflowExecution':1
        },
        'sdb': {
            'BatchDeleteAttributes': 1,
            'BatchPutAttributes':1,
            'CreateDomain':1
        },
        'storagegateway': {
            'ActivateGateway': 1,
            'AddCache':1,
            'AddUploadBuffer':1
        },
        'waf': {
            'CreateByteMatchSet': 1,
            'CreateIPSet':1,
            'CreateRule':1
        },
        'workspaces': {
            'CreateWorkspaces': 1,
            'DescribeWorkspaceBundles':1,
            'DescribeWorkspaceDirectories':1
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

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)
    client = session.client('iam')

    print("\n")
    policy_name = raw_input("Enter policy name: [ENTER]")

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
        response = client.create_policy(
            PolicyName=policy_name,
            Path='/',
            PolicyDocument='{"Version": "2012-10-17","Statement": [{"Effect":"' +
            str(effect_answer) +
            '","Action":["' +
            str(selected_service) +
            ':' +
            str(action) +
            '"],"Resource":"' +
            str(account_id) +
            '"}]}',
            Description='string')

        ################################
        # Example policy documents
        ################################

        #"PolicyDocument": {
        #       "Version" : "2012-10-17",
        #       "Statement": [ {
        #          "Effect": "Allow",
        #          "Action": "*",
        #          "Resource": "*"
        #} ]

        #"PolicyDocument": {
        #       "Version" : "2012-10-17",
        #       "Statement": [ {
        #          "Effect": "Allow",
        #          "Action": "*",
        #          "Resource": "*"
        #       } ]

        #"PolicyDocument": {
        #   "Statement": [{
        #   "Effect": "Allow",
        #   "Action": ["ec2:DescribeInstances", "ec2:DescribeRouteTables", "ec2:CreateRoute", "ec2:ReplaceRoute", "ec2:StartInstances", "ec2:StopInstances"],
        #       "Resource": "*"
        #     }]
        #},

        #"PolicyDocument": {
        #   "Statement": [{
        #       "Effect": "Allow",
        #       "Action": ["s3:GetObject"],
        #       "Resource": {
        #             "Fn::Join": ["", ["arn:aws:s3:::", {
        #           "Ref": "AWS::StackName"
        #             }, "/*"]]
        #       }
        #   }]
        #},

        #"PolicyDocument" : {
        #    "Version": "2012-10-17",
        #    "Statement" : [ {
        #       "Effect" : "Allow",
        #       "Action" : [ "sns:*" ],
        #       "Resource" : [ { "Ref" : "mytopic" } ]
        #    }, {
        #       "Effect" : "Deny",
        #       "Action" : [ "sns:*" ],
        #       "NotResource" : [ { "Ref" : "mytopic" } ]
        #    } ]
        # }

        #"PolicyDocument" : {
        #    "Version": "2012-10-17",
        #    "Statement" : [ {
        #       "Effect" : "Allow",
        #       "Action" : [
        #          "s3:GetObject" , "s3:PutObject" , "s3:PutObjectAcl" ],
        #       "Resource" : "arn:aws:s3:::myAWSBucket/*"
        #    } ]
        #},

        #"PolicyDocument" : {
        #    "Id" : "MyPolicy",
        #    "Version": "2012-10-17",
        #    "Statement" : [ {
        #       "Sid" : "ReadAccess",
        #       "Action" : [ "s3:GetObject" ],
        #       "Effect" : "Allow",
        #       "Resource" : { "Fn::Join" : [
        #             "", [ "arn:aws:s3:::", { "Ref" : "mybucket" } , "/*" ]
        #          ] },
        #       "Principal" : {
        #          "AWS" : { "Fn::GetAtt" : [ "user1", "Arn" ] }
        #       }
        #    } ]
        #},

        print(pretty(response))

    elif selected_service == 's3':

        resource = raw_input("Enter resource: [ENTER]")
    else:
        print(
            print("\n")
            print("###############################################################")
            print('Sorry, we have not programmed the functionality for the ' +
            str(selected_service) +
            ' service.')
            print("Functionality should be added soon.")
            print("################################################################")
        sys.exit


except (KeyboardInterrupt, SystemExit):
    sys.exit()
