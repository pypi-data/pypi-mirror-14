
import boto3.session


def list_hosted_zones(session):

    client = session.client('route53')
    response = client.list_hosted_zones()
    return response


def list_resource_record_sets(session,id):
    client = session.client('route53')


    response = client.list_resource_record_sets()
    return response
