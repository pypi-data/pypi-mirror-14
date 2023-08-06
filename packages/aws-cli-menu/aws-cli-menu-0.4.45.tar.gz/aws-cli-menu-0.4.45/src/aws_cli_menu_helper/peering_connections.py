
import re
import boto3.session

DEBUG =0




def get_peering_connections(session):

    client = session.resource('ec2')

    peering_connections = []

    for vpc_peering_connection_iterator in client.vpc_peering_connections.all():

        pc = {}

        vpc_pc_id = vpc_peering_connection_iterator.id

        pc['pc_id']= vpc_pc_id


        accepter_owner_id = vpc_peering_connection_iterator.accepter_vpc_info['OwnerId']
        accepter_vpc_id = vpc_peering_connection_iterator.accepter_vpc_info['VpcId']

        pc['accepter_owner_id'] = accepter_owner_id
        pc['accepter_vpc_id'] = accepter_vpc_id


        requester_owner_id = vpc_peering_connection_iterator.requester_vpc_info['OwnerId']
        requester_vpc_id = vpc_peering_connection_iterator.requester_vpc_info['VpcId']
        requester_cidr_block = vpc_peering_connection_iterator.requester_vpc_info['CidrBlock']

        pc['requester_owner_id']=requester_owner_id
        pc['requester_vpc_id'] = requester_vpc_id
        pc['requester_cidr_block'] = requester_cidr_block


        status = vpc_peering_connection_iterator.status['Message']
        status_code = vpc_peering_connection_iterator.status['Code']

        pc['status'] = status
        pc['status_code'] = status_code

        tags = vpc_peering_connection_iterator.tags

        if len(tags) >0:
            pc['tags'] = tags
        else:
            pc['tags']= []


        peering_connections.append(pc)


    return peering_connections