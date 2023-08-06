
import boto3.session
import sys


def get_iam_roles(session):

    try:
        client = session.client('iam')
        response = client.list_roles()
        stacks = response.get('Roles')

        menu = {}
        fields = {}

        for s in stacks:
            list=[]
            name = str(s.get('RoleName'))
            id = str(s.get('RoleId'))
            list.append(name)
            list.append(id)
            fields[name] = list

        counter = 0
        for item in sorted(fields):
            counter = counter +1
            menu[counter] = fields[item]

        return menu

    except (KeyboardInterrupt, SystemExit):
        sys.exit()



def get_role_info(session,id):

    try:
        client = session.client('iam')
        response = client.get_role(RoleName=str(id))
        stacks = response.get('Role')
        return stacks

    except (KeyboardInterrupt, SystemExit):
        sys.exit()

def print_role_menu(menu):

    try:

        print "\n\n"
        print '#############################'
        print '## Select Role             ##'
        print '#############################'
        for key in sorted(menu):
            print str(key)+":" + menu[key][0]

        return

    except (KeyboardInterrupt, SystemExit):
        sys.exit()