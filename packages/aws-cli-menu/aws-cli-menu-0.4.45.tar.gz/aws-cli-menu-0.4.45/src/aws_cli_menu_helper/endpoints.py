
import re
import boto3.session

DEBUG =0


def get_endpoints(session):

    client = session.client('ec2')
    response = client.describe_vpc_endpoint_services()


    return response



