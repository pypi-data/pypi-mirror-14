
import boto3.session


def describe_db_clusters(session):

    client = session.client('rds')
    response = client.describe_db_clusters()
    return response

def describe_db_instances(session):
    client = session.client('rds')
    response = client.describe_db_instances()
    return response


