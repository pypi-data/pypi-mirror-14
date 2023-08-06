#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys


try:

    profile_name = get_profile_name()

    session = boto3.session.Session(profile_name=profile_name)


    client = session.client('ecs')


    definition_name='hello-world-task'
    container_name='hello-world-container'
    #container_name='test'
    docker_image_to_run='training/webapp:latest'
    memory=128
    host_port=80
    container_port=5000
    #container_port=80
    protocol='tcp'


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

except (KeyboardInterrupt, SystemExit):
    sys.exit()
