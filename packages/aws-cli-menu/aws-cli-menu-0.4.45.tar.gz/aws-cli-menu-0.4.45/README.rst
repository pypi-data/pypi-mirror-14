**************
AWS CLI Menu
**************



A menu system for AWS CLI.
===========================

Why
------------
I got tired of running 3 to 4 different browsers to manage AWS accounts, and decided
to do everything command-line with boto3 and AWS CLI.

Note:  This is still a work in progress, but continue to check-in because I'm trying
to add new functionality daily.  I hope to have a polished product in several months.


Requirements
==============

- pyyaml
- six
- jinja2
- boto3


Example
============

.. code-block:: bash

    +------------------------------------------------------------------------------
    Main Menu
    +------------------------------------------------------------------------------
    [1] | All/General/Other
    [2] | API Gateway
    [3] | Cloud Formation
    [4] | Cloud Watch
    [5] | Dynamo DB
    [6] | EC2
    [7] | Elastic Cache
    [8] | IAM
    [9] | RDS
    [10] | Route53
    [11] | S3
    [12] | SNS
    [13] | SQS
    [14] | Support
    [15] | Tags
    [16] | VPC
    +------+-----------------------------------------------------------------------
    [0] | Quit
    +------------------------------------------------------------------------------



Installation
=============
`pip install aws-cli-menu`. This will install the scripts in /usr/share/aws-cli-menu folder.

Note: Install manually with 'sudo -H python setup.py install' if not installing with pip.

Note:  Make sure your ~/.aws config and credentials files are setup correctly with the profile
to the various AWS instances.


Example config:
=================

.. code-block:: bash

    [default]
    output = json
    region = us-east-1

    [profile test1]
    output = json
    region = us-east-1

    [profile test2]
    output = json
    region = us-east-1



Example credentials:
======================

.. code-block:: bash

    [default]
    aws_access_key_id = xxx
    aws_secret_access_key = xxx

    [test1]
    aws_access_key_id = xxx
    aws_secret_access_key = xxx

    [test2]
    aws_access_key_id = xx
    aws_secret_access_key = xxx



For script usage, run the following command:

.. code-block:: bash

    aws-cli-menu


Configuration
===============
If you want to add more scripts or modify the menu, got to /usr/share/aws-cli-menu and edit the aws-cli-menu.yml file and
add the scripts to the scripts directory.

It is best to follow the same yml format in the menu file, and the same format in the bash scripts.



Updates
==========
- 12/21/15 - Added ability to manage group policies
- 12/22/15 - Added ability to manage user and role policies
- 12/23/15 - Added ability to list tables in dynamodb and began work on policy creation function
- 12/24/15 - Added ability to create and delete dynamodb tables
- 12/26/15 - Added some simple network acl management
- 12/27/15 - Added elastic ip management and fixed policy creation and deletion
- 12/29/15 - Added ability to create and manage certificates and elastic load balancers
- 12/29/15 - Added ability to attach instance to load balancer
- 12/30/15 - Added sns management, route53 traffic policies and record sets, and cf template listing, and more
- 12/31/15 - Added NAT Gateways, Security Group and SQS Queue creation and deletion features
- 12/31/15 - Added User Login Profiles, User Access Keys, Role Policies, and Interfaces
- 12/31/15 - Added MFA Management
- 1/1/16 -   Added ability to attach, detach and manage volumes and network interfaces
- 1/2/16 -   Added Tagging of resources, snapshot creation and deletion, and fixed route tables
- 1/3/16 -   Clean-up a lot of the formatting and errors
- 1/3/16 -   Fixed stopped and starting of instances
- 1/4/16 -   Added more policy features
- 1/5/16 -   Added account alias, customer gateway, reserved instances and fixed auto scaling policy
- 1/7/16 -   Added ability to create cloud watch alarm and fixed a few other things
- 1/7/16 -   Fixed volume creation and deletion
- 1/8/16 -   Added RDS security groups and associated functionality
- 1/8/16 -   Added ability to modify rds instance
- 1/9/16 -   Added Elastic Cache functions
- 1/10/16 -  Refactored so menu matches AWS menu system
- 1/10/16 -  Added functions for vpn connection, gateway and customer gateway
- 1/10/16 -  Started adding functions to API Gateway and setup for virtualenv
- 1/11/16 -  Added EC2 Dashboard
- 1/12/16 -  Added RDS Dashboard and enhanced EC2 dashboard
- 1/13/16 -  Added VPC Dashboard
- 3/3/16 -   Added an All-Accounts option to get summary details for all accounts


Copyright
===========

Copyright 2015 Will Rubel

Based on easy-menu python module by mogproject.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
