from os.path import expanduser
import re
import cStringIO,operator
import math
import random
import sys
from .pretty import *

DEBUG = 0


def select_region():

    menu = {
        1:'us-east-1',  # Virginia
        2:'us-west-1',  # Northern California
        3:'us-west-2',  # Oregon
        4:'eu-west-1',  # Ireland
        5:'eu-central-1',  # Frankfurt
        6:'ap-southeast-1',  # Singapore
        7:'ap-southeast-2',  # Tokyo
        8:'sa-east-1'  # Soa Paulo


    }

    title = 'Select Region'
    print "\n"
    print('#' * len(title))
    print(str(title))
    print ('#'*len(title))
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER]")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                answer = menu[int(ans)]
                break

    return answer



def yes_or_no(title):

    menu = {1:['Yes',True],2:['No',False]}


    print "\n"
    print('#' * len(title))
    print(str(title))
    print ('#'*len(title))
    for key in sorted(menu):
        print str(key) + ":" + menu[key][0]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER]")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                answer = menu[int(ans)][1]
                break

    return answer



def generate_password():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    pw_length = 16
    mypw = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]

    # replace 1 or 2 characters with a number
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(mypw)//2)
        mypw = mypw[0:replace_index] + str(random.randrange(10)) + mypw[replace_index+1:]

    # replace 1 or 2 letters with an uppercase letter
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(mypw)//2,len(mypw))
        mypw = mypw[0:replace_index] + mypw[replace_index].upper() + mypw[replace_index+1:]

    return mypw


def get_all_profiles():
        home = expanduser("~")
        cred_file = home+'/.aws/credentials'

        lines = [line.rstrip('\n') for line in open(cred_file)]

        profiles = []
        for line in lines:
                matchObj = re.match( r'^\s*\[(.*)\]\s*$', line, re.M|re.I)
                if matchObj:
                   profiles.append(matchObj.group(1))

        return profiles

def get_profiles():

        if (DEBUG):
            print('terminalpy - get_profile(self)- caller:'+str(inspect.stack()[1][3]))

        home = expanduser("~")
        cred_file = home+'/.aws/credentials'

        lines = [line.rstrip('\n') for line in open(cred_file)]

        profiles = []
        for line in lines:
                matchObj = re.match( r'^\s*\[(.*)\]\s*$', line, re.M|re.I)
                if matchObj:
                   profiles.append(matchObj.group(1))


        menu = {}
        counter = 0
        for profile in sorted(profiles):
            counter = counter +1
            menu[counter] = profile

        return menu

def print_profile_menu(menu):
        for key in sorted(menu):
                print str(key)+":" + menu[key]

def get_profile_name():
    profiles = get_profiles()


    print("###############################")
    print("Select profile name")
    print("###############################")

    print_profile_menu(profiles)
    return get_profile_answer(profiles)


def get_profile_answer(profiles):
    pattern = r'^[0-9]+$'
    while True:

        profile = raw_input("Enter profile name [ENTER]:")
        if re.match(pattern,profile) is not None:
            if int(profile) in profiles:
                profile_name = profiles[int(profile)]
                break
            elif int(profile) == 0:
                sys.exit(1)

    return profile_name


def indent(rows, hasHeader=False, headerChar='-', delim=' | ', justify='left',
           separateRows=False, prefix='', postfix='', wrapfunc=lambda x:x):
    """Indents a table by column.
       - rows: A sequence of sequences of items, one sequence per row.
       - hasHeader: True if the first row consists of the columns' names.
       - headerChar: Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
       - delim: The column delimiter.
       - justify: Determines how are data justified in their column.
         Valid values are 'left','right' and 'center'.
       - separateRows: True if rows are to be separated by a line
         of 'headerChar's.
       - prefix: A string prepended to each printed row.
       - postfix: A string appended to each printed row.
       - wrapfunc: A function f(text) for wrapping text; each element in
         the table is first wrapped by this function."""
    # closure for breaking logical rows to physical, using wrapfunc
    def rowWrapper(row):
        newRows = [wrapfunc(item).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in map(None,*newRows)]


    # break each logical row into one or more physical ones
    logicalRows = [rowWrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None,*reduce(operator.add,logicalRows))
    # get the maximum of each column by the string length of its items
    maxWidths = [max([len(str(item)) for item in column]) for column in columns]
    rowSeparator = headerChar * (len(prefix) + len(postfix) + sum(maxWidths) + \
                                 len(delim)*(len(maxWidths)-1))
    # select the appropriate justify method
    justify = {'center':str.center, 'right':str.rjust, 'left':str.ljust}[justify.lower()]
    output=cStringIO.StringIO()
    if separateRows: print >> output, rowSeparator
    for physicalRows in logicalRows:
        for row in physicalRows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item),width) for (item,width) in zip(row,maxWidths)]) \
                + postfix
        if separateRows or hasHeader: print >> output, rowSeparator; hasHeader=False
    return output.getvalue()

# written by Mike Brown
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """

    if type(text) is str:
        return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )
    elif type(text) is list:
        new_text = ''
        counter = 0
        for e in text:
            counter += 1
            new_text += '('+str(counter)+') '+str(e)+"\n"
        #new_text = ''.join(str(e) for e in text)
        return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line[line.rfind('\n')+1:])
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  new_text.split(' ')
                 )



def wrap_onspace_strict(text, width):
    """Similar to wrap_onspace, but enforces the width constraint:
       words longer than width are split."""
    wordRegex = re.compile(r'\S{'+str(width)+r',}')

    if type(text) is str:

        return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(),width),text),width)
    elif type(text) is list:
        new_text = ''
        counter = 0
        for e in text:
            counter += 1
            new_text += '('+str(counter)+') '+str(e)+"\n"
        #new_text = ''.join(str(e) for e in text)
        return wrap_onspace(wordRegex.sub(lambda m: wrap_always(m.group(),width),new_text),width)



def wrap_always(text, width):
    """A simple word-wrap function that wraps text on exactly width characters.
       It doesn't split the text in words."""

    if type(text) is str:
        return '\n'.join([ text[width*i:width*(i+1)] for i in xrange(int(math.ceil(1.*len(text)/width))) ])
    elif type(text) is list:

        new_text = ''
        counter = 0
        for e in text:
            counter += 1
            new_text += '('+str(counter)+') '+str(e)+"\n"
        #new_text = ''.join(str(e) for e in text)
        return '\n'.join([ new_text[width*i:width*(i+1)] for i in xrange(int(math.ceil(1.*len(new_text)/width))) ])


def delete_tags(session, resource_id,key,value):

    client = session.client('ec2')

    response = client.delete_tags(
        DryRun=False,
        Resources=[resource_id],
        Tags=[
            {
                'Key': key,
                'Value': value
            }
        ]
    )

    print("\n")
    print(pretty(response))

    return