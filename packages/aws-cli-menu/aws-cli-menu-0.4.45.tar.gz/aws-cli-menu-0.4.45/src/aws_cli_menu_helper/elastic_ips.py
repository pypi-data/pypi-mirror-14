
import re
import boto3.session

DEBUG =0


def get_elastic_ips(session):

    client = session.client('ec2')

    response = client.describe_addresses()
    stacks = response.get('Addresses')

    return stacks