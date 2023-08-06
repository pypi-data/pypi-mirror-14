
import boto3.session





def get_iam_users(session):

    client = session.client('iam')
    response = client.list_users()
    stacks = response.get('Users')

    menu = {}
    fields = {}

    for s in stacks:
        list=[]
        name = str(s.get('UserName'))
        id = str(s.get('UserId'))
        list.append(name)
        list.append(id)
        fields[name] = list

    counter = 0
    for item in sorted(fields):
        counter = counter +1
        menu[counter] = fields[item]

    return menu


def get_user_info(session,name):
    client = session.client('iam')


    response = client.get_user(UserName=str(name))
    stacks = response.get('User')
    return stacks




def print_user_menu(menu):

    for key in sorted(menu):
        print str(key)+":" + menu[key][0]

    return


def get_account_id(session,name):
    client = session.client('iam')


    response = client.get_user(UserName=str(name))
    stacks = response.get('User')
    arn = stacks['Arn']
    return arn