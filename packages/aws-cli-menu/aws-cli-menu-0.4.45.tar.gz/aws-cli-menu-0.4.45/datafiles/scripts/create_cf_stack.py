#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import collections
import json
import time

try:

    profile_name = get_profile_name()
    print("\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('cloudformation')

    stack_name = raw_input("Enter stack name: [ENTER](Cntrl-C to exit)")
    key_name = raw_input("Enter key name: [ENTER](Cntrl-C to exit)")
    cluster_name = raw_input("Enter cluster name: [ENTER](Cntrl-C to exit)")

    if (1):


        template_body = collections.OrderedDict()


        template_body['AWSTemplateFormatVersion']='2010-09-09'
        template_body['Description']='ECS CF Script'
        template_body['Parameters']={}
        template_body['Parameters']['INSTANCENAME']={
            "Description":"The name of the instance",
            "Type":"String",
            "Default":"test"
        }

        template_body['Parameters']['EcsInstanceType']={
            "Type":"String",
            "Description":"ECS EC2 Instance Type",
            "Default":"t2.micro",
            "AllowedValues":[
                "t2.micro"
            ]
        }

        template_body['Parameters']['KeyName']={
            "Type":"String",
            "Description":"Optional - Name of an existing EC2 KeyPair to enable SSH access to the ECS instances.",
            "Default":""
        }

        template_body['Parameters']['VpcId']={
            "Type":"String",
            "Description":"Optional - VPC Id of existing VPC. Leave blank to have a VPC created",
            "Default":"",
            "AllowedPattern":"^(?:vpc-[0-9a-f]{8}|)$"
        }

        template_body['Parameters']['SubnetIds']= {
          "Type": "CommaDelimitedList",
          "Description": "Optional - Comma separated list of existing VPC Subnet Ids where ECS instances will run",
          "Default": ""
        }

        template_body['Parameters']['AsgDesiredSize']={
          "Type": "Number",
          "Description": "Initial Desired Capacity of ECS Auto Scaling Group",
          "Default": "1"
        }

        template_body['Parameters']['EcsClusterName']={
          "Type": "String",
          "Description": "ECS Cluster Name",
          "Default": "default"
        }

        template_body['Parameters']['EcsPort']={
          "Type": "String",
          "Description": "Optional - Security Group port to open on ECS instances - defaults to port 80",
          "Default": "80"
        }

        template_body['Parameters']['ElbPort']={
          "Type": "String",
          "Description": "Optional - Security Group port to open on ELB - port 80 will be open by default",
          "Default": "80"
        }

        template_body['Parameters']['ElbProtocol']={
          "Type": "String",
          "Description": "Optional - ELB Protocol - defaults to HTTP",
          "Default": "HTTP"
        }

        template_body['Parameters']['ElbHealthCheckTarget']={
          "Type": "String",
          "Description": "Optional - Health Check Target for ELB - defaults to HTTP:80/",
          "Default": "HTTP:80/"
        }

        template_body['Parameters']['SourceCidr']={
          "Type": "String",
          "Description": "Optional - CIDR/IP range for EcsPort and ElbPort - defaults to 0.0.0.0/0",
          "Default": "0.0.0.0/0"
        }

        template_body['Parameters']['EcsEndpoint']={
          "Type": "String",
          "Description": "Optional : ECS Endpoint for the ECS Agent to connect to",
          "Default": ""
        }

        template_body['Parameters']['CreateElasticLoadBalancer']={
          "Type": "String",
          "Description": "Optional : When set to true, creates a ELB for ECS Service",
          "Default": "true"
        }


        template_body['Parameters']['VpcAvailabilityZones']={
          "Type": "CommaDelimitedList",
          "Description": "Optional : Comma-delimited list of two VPC availability zones in which to create subnets",
          "Default": ""
        }

        template_body['Conditions']={}

        template_body['Conditions']['CreateVpcResources']={
          "Fn::Equals": [{"Ref": "VpcId"},""]
        }

        template_body['Conditions']['ExistingVpcResources']={
          "Fn::Not": [
            {
              "Fn::Equals": [
                {
                  "Ref": "VpcId"
                },
                ""
              ]
            }
          ]
        }

        template_body['Conditions']['SetEndpointToECSAgent']={
          "Fn::Not": [
            {
              "Fn::Equals": [
                {
                  "Ref": "EcsEndpoint"
                },
                ""
              ]
            }
          ]
        }


        template_body['Conditions']['CreateELBForExistingVpc']={
          "Fn::And": [
            {
              "Fn::Equals": [
                {
                  "Ref": "CreateElasticLoadBalancer"
                },
                "true"
              ]
            },
            {
              "Condition": "ExistingVpcResources"
            }
          ]
        }


        template_body['Conditions']['CreateELBForNewVpc']={
          "Fn::And": [
            {
              "Fn::Equals": [
                {
                  "Ref": "CreateElasticLoadBalancer"
                },
                "true"
              ]
            },
            {
              "Condition": "CreateVpcResources"
            }
          ]
        }

        template_body['Conditions']['CreateELB']={
          "Fn::Or": [
            {
              "Condition": "CreateELBForExistingVpc"
            },
            {
              "Condition": "CreateELBForNewVpc"
            }
          ]
        }

        template_body['Conditions']['CreateEC2LCWithKeyPair']={
          "Fn::Not": [
            {
              "Fn::Equals": [
                {
                  "Ref": "KeyName"
                },
                ""
              ]
            }
          ]
        }

        template_body['Conditions']['CreateEC2LCWithoutKeyPair']={
          "Fn::Equals": [
            {
              "Ref": "KeyName"
            },
            ""
          ]
        }

        template_body['Conditions']['UseSpecifiedVpcAvailabilityZones']={
          "Fn::Not": [
            {
              "Fn::Equals": [
                {
                  "Fn::Join": [
                    "",
                    {
                      "Ref": "VpcAvailabilityZones"
                    }
                  ]
                },
                ""
              ]
            }
          ]
        }



        template_body['Mappings']={}

        template_body['Mappings']['VpcCidrs']={
            "us-east-1":{
                "vpc": "10.0.0.0/16",
                "pubsubnet1": "10.0.0.0/24",
                "pubsubnet2": "10.0.1.0/24"
            }
        }
        template_body['Mappings']['EcsAmiIds']={
            "us-east-1":{
                "id":"ami-b540eade"
            }
        }

        template_body['Resources']={}
        template_body['Resources']['Vpc']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::VPC",
          "Properties": {
            "CidrBlock": {
              "Fn::FindInMap": [
                "VpcCidrs",
                {
                  "Ref": "AWS::Region"
                },
                "vpc"
              ]
            },
            "EnableDnsSupport": "true",
            "EnableDnsHostnames": "true"
          }
        }

        template_body['Resources']['PubSubnetAz1']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::Subnet",
          "Properties": {
            "VpcId": {
              "Ref": "Vpc"
            },
            "CidrBlock": {
              "Fn::FindInMap": [
                "VpcCidrs",
                {
                  "Ref": "AWS::Region"
                },
                "pubsubnet1"
              ]
            },
            "AvailabilityZone": {
              "Fn::If": [
                "UseSpecifiedVpcAvailabilityZones",
                {
                  "Fn::Select": [
                    "0",
                    {
                      "Ref": "VpcAvailabilityZones"
                    }
                  ]
                },
                {
                  "Fn::Select": [
                    "0",
                    {
                      "Fn::GetAZs": {
                        "Ref": "AWS::Region"
                      }
                    }
                  ]
                }
              ]
            }
          }
        }

        template_body['Resources']['PubSubnetAz2']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::Subnet",
          "Properties": {
            "VpcId": {
              "Ref": "Vpc"
            },
            "CidrBlock": {
              "Fn::FindInMap": [
                "VpcCidrs",
                {
                  "Ref": "AWS::Region"
                },
                "pubsubnet2"
              ]
            },
            "AvailabilityZone": {
              "Fn::If": [
                "UseSpecifiedVpcAvailabilityZones",
                {
                  "Fn::Select": [
                    "1",
                    {
                      "Ref": "VpcAvailabilityZones"
                    }
                  ]
                },
                {
                  "Fn::Select": [
                    "1",
                    {
                      "Fn::GetAZs": {
                        "Ref": "AWS::Region"
                      }
                    }
                  ]
                }
              ]
            }
          }
        }

        template_body['Resources']['InternetGateway']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::InternetGateway"
        }


        template_body['Resources']['AttachGateway']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::VPCGatewayAttachment",
          "Properties": {
            "VpcId": {
              "Ref": "Vpc"
            },
            "InternetGatewayId": {
              "Ref": "InternetGateway"
            }
          }
        }

        # Route via the internet gateway
        template_body['Resources']['RouteViaIgw']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::RouteTable",
          "Properties": {
            "VpcId": {
              "Ref": "Vpc"
            }
          }
        }

        template_body['Resources']['PublicRouteViaIgw']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::Route",
          "Properties": {
            "RouteTableId": {
              "Ref": "RouteViaIgw"
            },
            "DestinationCidrBlock": "0.0.0.0/0",
            "GatewayId": {
              "Ref": "InternetGateway"
            }
          }
        }

        template_body['Resources']['PubSubnet1RouteTableAssociation']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::SubnetRouteTableAssociation",
          "Properties": {
            "SubnetId": {
              "Ref": "PubSubnetAz1"
            },
            "RouteTableId": {
              "Ref": "RouteViaIgw"
            }
          }
        }

        template_body['Resources']['PubSubnet2RouteTableAssociation']={
          "Condition": "CreateVpcResources",
          "Type": "AWS::EC2::SubnetRouteTableAssociation",
          "Properties": {
            "SubnetId": {
              "Ref": "PubSubnetAz2"
            },
            "RouteTableId": {
              "Ref": "RouteViaIgw"
            }
          }
        }

        template_body['Resources']['ElbSecurityGroup']={
          "Type": "AWS::EC2::SecurityGroup",
          "Properties": {
            "GroupDescription": "ELB Allowed Ports",
            "VpcId": {
              "Fn::If": [
                "CreateVpcResources",
                {
                  "Ref": "Vpc"
                },
                {
                  "Ref": "VpcId"
                }
              ]
            },
            "SecurityGroupIngress": [
              {
                "IpProtocol": "tcp",
                "FromPort": {
                  "Ref": "ElbPort"
                },
                "ToPort": {
                  "Ref": "ElbPort"
                },
                "CidrIp": {
                  "Ref": "SourceCidr"
                }
              }
            ]
          }
        }


        template_body['Resources']['EcsSecurityGroup']={
          "Type": "AWS::EC2::SecurityGroup",
          "Properties": {
            "GroupDescription": "ECS Allowed Ports",
            "VpcId": {
              "Fn::If": [
                "CreateVpcResources",
                {
                  "Ref": "Vpc"
                },
                {
                  "Ref": "VpcId"
                }
              ]
            },
            "SecurityGroupIngress": {
              "Fn::If": [
                "CreateELB",
                [
                  {
                    "IpProtocol": "tcp",
                    "FromPort": {
                      "Ref": "EcsPort"
                    },
                    "ToPort": {
                      "Ref": "EcsPort"
                    },
                    "CidrIp": {
                      "Ref": "SourceCidr"
                    }
                  },
                  {
                    "IpProtocol": "tcp",
                    "FromPort": "1",
                    "ToPort": "65535",
                    "SourceSecurityGroupId": {
                      "Ref": "ElbSecurityGroup"
                    }
                  }
                ],
                [
                  {
                    "IpProtocol": "tcp",
                    "FromPort": {
                      "Ref": "EcsPort"
                    },
                    "ToPort": {
                      "Ref": "EcsPort"
                    },
                    "CidrIp": {
                      "Ref": "SourceCidr"
                    }
                  }
                ]
              ]
            }
          }
        }

        template_body['Resources']['EcsElasticLoadBalancer']={
          "Condition": "CreateELBForNewVpc",
          "Type": "AWS::ElasticLoadBalancing::LoadBalancer",
          "Properties": {
            "SecurityGroups": [
              {
                "Ref": "ElbSecurityGroup"
              }
            ],
            "Subnets": [
              {
                "Ref": "PubSubnetAz1"
              },
              {
                "Ref": "PubSubnetAz2"
              }
            ],
            "CrossZone": "true",
            "Listeners": [
              {
                "LoadBalancerPort": {
                  "Ref": "ElbPort"
                },
                "InstancePort": {
                  "Ref": "EcsPort"
                },
                "Protocol": {
                  "Ref": "ElbProtocol"
                }
              }
            ],
            "HealthCheck": {
              "Target": {
                "Ref": "ElbHealthCheckTarget"
              },
              "HealthyThreshold": "2",
              "UnhealthyThreshold": "10",
              "Interval": "30",
              "Timeout": "5"
            }
          }
        }

        template_body['Resources']['EcsElasticLoadBalancerExistingVpc']={
          "Condition": "CreateELBForExistingVpc",
          "Type": "AWS::ElasticLoadBalancing::LoadBalancer",
          "Properties": {
            "SecurityGroups": [
              {
                "Ref": "ElbSecurityGroup"
              }
            ],
            "Subnets": {
              "Ref": "SubnetIds"
            },
            "CrossZone": "true",
            "Listeners": [
              {
                "LoadBalancerPort": {
                  "Ref": "ElbPort"
                },
                "InstancePort": {
                  "Ref": "EcsPort"
                },
                "Protocol": {
                  "Ref": "ElbProtocol"
                }
              }
            ],
            "HealthCheck": {
              "Target": {
                "Ref": "ElbHealthCheckTarget"
              },
              "HealthyThreshold": "2",
              "UnhealthyThreshold": "10",
              "Interval": "30",
              "Timeout": "5"
            }
          }
        }

        template_body['Resources']['EcsInstanceLc']={
          "Condition": "CreateEC2LCWithKeyPair",
          "Type": "AWS::AutoScaling::LaunchConfiguration",
          "Properties": {
            "ImageId": {
              "Fn::FindInMap": [
                "EcsAmiIds",
                {
                  "Ref": "AWS::Region"
                },
                "id"
              ]
            },
            "InstanceType": {
              "Ref": "EcsInstanceType"
            },
            "AssociatePublicIpAddress": True,
            "IamInstanceProfile": {
              "Ref": "EcsInstanceProfile"
            },
            "KeyName": {
              "Ref": "KeyName"
            },
            "SecurityGroups": [
              {
                "Ref": "EcsSecurityGroup"
              }
            ],
            "UserData": {
              "Fn::If": [
                "SetEndpointToECSAgent",
                {
                  "Fn::Base64": {
                    "Fn::Join": [
                      "",
                      [
                        "#!/bin/bash\n",
                        "echo ECS_CLUSTER=",
                        {
                          "Ref": "EcsClusterName"
                        },
                        " >> /etc/ecs/ecs.config",
                        "\necho ECS_BACKEND_HOST=",
                        {
                          "Ref": "EcsEndpoint"
                        },
                        " >> /etc/ecs/ecs.config"
                      ]
                    ]
                  }
                },
                {
                  "Fn::Base64": {
                    "Fn::Join": [
                      "",
                      [
                        "#!/bin/bash\n",
                        "echo ECS_CLUSTER=",
                        {
                          "Ref": "EcsClusterName"
                        },
                        " >> /etc/ecs/ecs.config"
                      ]
                    ]
                  }
                }
              ]
            }
          }
        }

        template_body['Resources']['EcsInstanceLcWithoutKeyPair']={
          "Condition": "CreateEC2LCWithoutKeyPair",
          "Type": "AWS::AutoScaling::LaunchConfiguration",
          "Properties": {
            "ImageId": {
              "Fn::FindInMap": [
                "EcsAmiIds",
                {
                  "Ref": "AWS::Region"
                },
                "id"
              ]
            },
            "InstanceType": {
              "Ref": "EcsInstanceType"
            },
            "AssociatePublicIpAddress": True,
            "IamInstancProfile": {
              "Ref": "EcsInstanceProfile"
            },
            "SecurityGroups": [
              {
                "Ref": "EcsSecurityGroup"
              }
            ],
            "UserData": {
              "Fn::If": [
                "SetEndpointToECSAgent",
                {
                  "Fn::Base64": {
                    "Fn::Join": [
                      "",
                      [
                        "#!/bin/bash\n",
                        "echo ECS_CLUSTER=",
                        {
                          "Ref": "EcsClusterName"
                        },
                        " >> /etc/ecs/ecs.config",
                        "\necho ECS_BACKEND_HOST=",
                        {
                          "Ref": "EcsEndpoint"
                        },
                        " >> /etc/ecs/ecs.config"
                      ]
                    ]
                  }
                },
                {
                  "Fn::Base64": {
                    "Fn::Join": [
                      "",
                      [
                        "#!/bin/bash\n",
                        "echo ECS_CLUSTER=",
                        {
                          "Ref": "EcsClusterName"
                        },
                        " >> /etc/ecs/ecs.config"
                      ]
                    ]
                  }
                }
              ]
            }
          }
        }

        # Auto Scaling Group
        template_body['Resources']['EcsInstanceAsg']={
          "Type": "AWS::AutoScaling::AutoScalingGroup",
          "Properties": {
        "LoadBalancerNames" :
              {
                "Fn::If": [
                  "CreateELBForNewVpc",
                  [ {
                    "Ref": "EcsElasticLoadBalancer"
                  } ],
                  [ {
                    "Ref": "EcsElasticLoadBalancerExistingVpc"
                  } ]
                ]
              },
            "AvailabilityZones": {
              "Fn::If": [
                "UseSpecifiedVpcAvailabilityZones",
                [
                  {
                    "Fn::Select": [
                      "0",
                      {
                        "Ref": "VpcAvailabilityZones"
                      }
                    ]
                  },
                  {
                    "Fn::Select": [
                      "1",
                      {
                        "Ref": "VpcAvailabilityZones"
                      }
                    ]
                  }
                ],
                [
                  {
                    "Fn::Select": [
                      "0",
                      {
                        "Fn::GetAZs": {
                          "Ref": "AWS::Region"
                        }
                      }
                    ]
                  },
                  {
                    "Fn::Select": [
                      "1",
                      {
                        "Fn::GetAZs": {
                          "Ref": "AWS::Region"
                        }
                      }
                    ]
                  }
                ]
              ]
            },
            "VPCZoneIdentifier": {
              "Fn::If": [
                "CreateVpcResources",
                [
                  {
                    "Fn::Join": [
                      ",",
                      [
                        {
                          "Ref": "PubSubnetAz1"
                        },
                        {
                          "Ref": "PubSubnetAz2"
                        }
                      ]
                    ]
                  }
                ],
                {
                  "Ref": "SubnetIds"
                }
              ]
            },
            "LaunchConfigurationName": {
              "Fn::If": [
                "CreateEC2LCWithKeyPair",
                {
                  "Ref": "EcsInstanceLc"
                },
                {
                  "Ref": "EcsInstanceLcWithoutKeyPair"
                }
              ]
            },
            "MinSize": "1",
            "MaxSize": "10",
            "DesiredCapacity": {
              "Ref": "AsgDesiredSize"
            },
            "Tags": [
              {
                "Key": "Name",
                "Value": {
                  "Fn::Join": [
                    "",
                    [
                      "ECS Instance - ",
                      {
                        "Ref": "AWS::StackName"
                      }
                    ]
                  ]
                },
                "PropagateAtLaunch": "true"
              }
            ]
          }
        }


        template_body['Resources']['EcsInstanceProfile']={
          "Type": "AWS::IAM::InstanceProfile",
          "Properties": {
            "Path": "/",
            "Roles": [
              {
                "Ref": "EcsInstanceRole"
              }
            ]
          }
        }

        template_body['Resources']['EcsInstanceRole']={
          "Type": "AWS::IAM::Role",
          "Properties": {
            "AssumeRolePolicyDocument": {
              "Version": "2008-10-17",
              "Statement": [
                {
                  "Action": "sts:AssumeRole",
                  "Principal": {
                    "Service": "ec2.amazonaws.com"
                  },
                  "Effect": "Allow",
                  "Sid": ""
                }
              ]
            },
            "Path": "/",
            "Policies": [
              {
                "PolicyName": "EcsInstance",
                "PolicyDocument": {
                  "Version": "2012-10-17",
                  "Statement": [
                    {
                      "Effect": "Allow",
                      "Action": [
                        "ecs:CreateCluster",
                        "ecs:DeregisterContainerInstance",
                        "ecs:DiscoverPollEndpoint",
                        "ecs:Poll",
                        "ecs:RegisterContainerInstance",
                        "ecs:StartTelemetrySession",
                        "ecs:Submit*"
                      ],
                      "Resource": [
                        "*"
                      ]
                    },
                    {
                      "Effect": "Allow",
                      "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "logs:DescribeLogStreams"
                      ],
                      "Resource": [
                        "arn:aws:logs:*:*:*"
                      ]
                    }
                  ]
                }
              }
            ]
          }
        }

        template_body['Resources']['EcsServiceRole']={
          "Type": "AWS::IAM::Role",
          "Properties": {
            "AssumeRolePolicyDocument": {
              "Version": "2008-10-17",
              "Statement": [
                {
                  "Sid": "",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": "ecs.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
                }
              ]
            },
            "Path": "/",
            "Policies": [
              {
                "PolicyName": "EcsService",
                "PolicyDocument": {
                  "Version": "2012-10-17",
                  "Statement": [
                    {
                      "Effect": "Allow",
                      "Action": [
                        "ec2:AuthorizeSecurityGroupIngress",
                        "ec2:Describe*",
                        "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                        "elasticloadbalancing:Describe*",
                        "elasticloadbalancing:RegisterInstancesWithLoadBalancer"
                      ],
                      "Resource": "*"
                    }
                  ]
                }
              }
            ]
          }
        }







        template_body['Outputs']={}


        template_body['Outputs']['EcsInstanceAsgName']={
          "Description": "Auto Scaling Group Name for ECS Instances",
          "Value": {
            "Ref": "EcsInstanceAsg"
          }
        }

        template_body['Outputs']['EcsServiceRole']={
            "Description":"Role name",
            "Value":{
                "Ref": "EcsServiceRole"
            }
        }


        template_body['Outputs']['EcsInstanceRole']={
            "Description":"Role name",
            "Value":{
                "Ref": "EcsInstanceRole"
            }
        }
        template_body['Outputs']['EcsElbName']={
          "Description": "Load Balancer for ECS Service",
          "Value": {
            "Fn::If": [
              "CreateELB",
              {
                "Fn::If": [
                  "CreateELBForNewVpc",
                  {
                    "Ref": "EcsElasticLoadBalancer"
                  },
                  {
                    "Ref": "EcsElasticLoadBalancerExistingVpc"
                  }

                ]
              },
              ""
            ]
          }
        }

        #order= [
        #    'AWSTemplateFormatVersion',
        #    'Description',
        #    'Mappings',
        #    'Parameters',
        #    'Conditions',
        #    'Resources',
        #    'Outputs'
        #]



        json_string = json.dumps(template_body)
        print(json_string)

        response = client.validate_template(
            TemplateBody=str(json_string)
            #TemplateURL='string'
        )

        print(pretty(response))

        response = client.create_stack(
            StackName=str(stack_name),
            TemplateBody=str(json_string),
            #TemplateURL='string',
            Parameters=[
                {
                    'ParameterKey': 'KeyName',
                    'ParameterValue': str(key_name),
                    'UsePreviousValue': False
                },
                {
                    'ParameterKey': 'EcsClusterName',
                    'ParameterValue': str(cluster_name),
                    'UsePreviousValue': False
                },
            ],
            DisableRollback=True,
            #DisableRollback=True|False,
            TimeoutInMinutes=10,
            #NotificationARNs=[
            #    'string',
            #],
            Capabilities=[
                'CAPABILITY_IAM',
            ],
            #ResourceTypes=[
            #    'string',
            #],
            #OnFailure='DELETE',
            #OnFailure='DO_NOTHING'|'ROLLBACK'|'DELETE',
            #StackPolicyBody='string',
            #StackPolicyURL='string',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'test'
                },
            ]
        )

        print(pretty(response))

        complete = -1

        while complete < 0:


            response = client.list_stacks(
                StackStatusFilter=[
                    'CREATE_IN_PROGRESS',
                    'CREATE_FAILED',
                    'CREATE_COMPLETE',
                    'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS',
                    'UPDATE_COMPLETE',
                    'UPDATE_IN_PROGRESS'])


            stacks = response.get('StackSummaries')


            if len(stacks) > 0:
                dict = {}

                for s in stacks:
                    list = []

                    if s.get('StackName') == str(stack_name):
                        print(s.get('StackStatus'))

                        if s.get('StackStatus') == 'CREATE_COMPLETE':
                            complete = 1


                time.sleep(5)

    elb_name = ''
    asg_name = ''
    instance_role = ''
    service_role = ''

    if (1):

        response = client.describe_stacks(
            StackName=str(stack_name)
        )

        print(pretty(response))

        stacks = response.get('Stacks')

        for i in stacks:
            print(pretty(i))
            if i['StackName']== str(stack_name):
                print('found it')
                print(pretty(i['Outputs']))
                for j in i['Outputs']:


                    if j['OutputKey'] == 'EcsElbName':
                        elb_name = j['OutputValue']
                    elif (j['OutputKey'] == 'EcsInstanceAsgName'):
                        asg_name = j['OutputValue']
                    elif (j['OutputKey'] == 'EcsInstanceRole'):
                        instance_role = j['OutputValue']
                    elif (j['OutputKey'] == 'EcsServiceRole'):
                        service_role = j['OutputValue']


        print('asg name: '+str(asg_name))
        print('elb name: '+str(elb_name))
        print('instance role: '+str(instance_role))







    client = session.client('ecs')


    definition_name='test'
    container_name=str(cluster_name)
    docker_image_to_run='training/webapp:latest'
    memory=128
    host_port=80
    container_port=80
    protocol='tcp'

    task_arn = ''




    if (0):
        response = client.create_cluster(
            clusterName=str(cluster_name)
        )

        print(pretty(response))

    if (1):

        response = client.register_task_definition(
            family=str(definition_name),
            containerDefinitions=[
                {
                    'name': str(container_name),
                    'image': str(docker_image_to_run),
                    #'cpu': 123,
                    'memory': memory,
                    #'links': [
                    #    'string',
                    #],
                    'portMappings': [
                        {
                            'containerPort': container_port,
                            'hostPort': host_port,
                            #'protocol': 'tcp'|'udp'
                            'protocol':str(protocol)
                        },
                    ],
                    'essential': True
                    #'entryPoint': [
                    #    'string',
                    #],
                    #'command': [
                    #    'string',
                    #],
                    #'environment': [
                    #    {
                    #        'name': 'string',
                    #        'value': 'string'
                    #    },
                    #],
                    #'mountPoints': [
                    #    {
                    #        'sourceVolume': 'string',
                    #        'containerPath': 'string',
                    #        'readOnly': True|False
                    #    },
                    #],
                    #'volumesFrom': [
                    #    {
                    #        'sourceContainer': 'string',
                    #        'readOnly': True|False
                    #    },
                    #],
                    #'hostname': 'string',
                    #'user': 'string',
                    #'workingDirectory': 'string',
                    #'disableNetworking': True|False,
                    #'privileged': True|False,
                    #'readonlyRootFilesystem': True|False,
                    #'dnsServers': [
                    #    'string',
                    #],
                    #'dnsSearchDomains': [
                    #    'string',
                    #],
                    #'extraHosts': [
                    #    {
                    #        'hostname': 'string',
                    #        'ipAddress': 'string'
                    #    },
                    #],
                    #'dockerSecurityOptions': [
                    #    'string',
                    #],
                    #'dockerLabels': {
                    #    'string': 'string'
                    #},
                    #'ulimits': [
                    #    {
                    #        'name': 'core'|'cpu'|'data'|'fsize'|'locks'|'memlock'|'msgqueue'|'nice'|'nofile'|'nproc'|'rss'|'rtprio'|'rttime'|'sigpending'|'stack',
                    #        'softLimit': 123,
                    #        'hardLimit': 123
                    #    },
                    #],
                    #'logConfiguration': {
                    #    'logDriver': 'json-file'|'syslog'|'journald'|'gelf'|'fluentd',
                    #    'options': {
                    #        'string': 'string'
                    #    }
                    #}
                },
            ],
            volumes=[
                {
                    'name': 'string',
                    'host': {
                        'sourcePath': 'string'
                    }
                },
            ]
        )

        print("\n")
        print(pretty(response))

        task_arn = response['taskDefinition']['taskDefinitionArn']
        response = client.describe_task_definition(
            taskDefinition=task_arn
        )

        print("\n")
        print(pretty(response))

        task_arn = response['taskDefinition']['taskDefinitionArn']
        container = response['taskDefinition']['containerDefinitions'][0]
        print('container: ')
        print(pretty(container))
        container_name = container['name']
        port_mappings = container['portMappings']
        print('port mappings:')
        print(pretty(port_mappings))
        container_port = port_mappings[0]['containerPort']

        print('container port: '+str(container_port))
        print('container name: '+str(container_name))



        desired_count =1
        print('asg name: '+str(asg_name))
        print('elb name: '+str(elb_name))
        print('instance role: '+str(instance_role))
        print('container name: '+str(container_name))
        print('container port: '+str(container_port))
        print('cluster name: '+str(cluster_name))
        print('task arn: '+str(task_arn))



        response = client.create_service(
            cluster=str(cluster_name),
            serviceName='test',
            taskDefinition=str(task_arn),
            loadBalancers=[
                {
                    'loadBalancerName': str(elb_name),
                    'containerName': str(container_name),
                    'containerPort': int(container_port)
                },
            ],
            desiredCount=desired_count,
        ##    clientToken='string',
            role=str(service_role)
        ##    deploymentConfiguration={
        ##        'maximumPercent': 123,
        ##        'minimumHealthyPercent': 123
        ##    }
        )

        print("\n")
        print(pretty(response))


except (KeyboardInterrupt, SystemExit):
    sys.exit()
