#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import os
import hashlib
import subprocess
import datetime

DEBUG = 1

try:

    OPENSSL_CONFIG_TEMPLATE = """
prompt = no
distinguished_name = req_distinguished_name
req_extensions = v3_req
[ req_distinguished_name ]
C = %(country_code)s
ST = %(state_code)s
L = %(locality)s
O = %(organization_name)s
OU = %(organizational_unit)s
CN = %(domain)s
emailAddress = %(email)s
[ v3_req ]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[ alt_names ]
DNS.1 = %(domain)s
DNS.2 = *.%(domain)s
"""

    MYDIR = raw_input(
        "Enter directory to store certificates (example: /tmp/): [ENTER]")

    def which(program):
        import os

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    OPENSSL = which('openssl')

    print('openssl is:' + str(OPENSSL))

    KEY_SIZE = 2048
    DAYS = 3650
    CA_CERT = 'ca.cert'
    CA_KEY = 'ca.key'

    # Extra X509 args. Consider using e.g. ('-passin', 'pass:blah') if your
    # CA password is 'blah'. For more information, see:
    #
    # http://www.openssl.org/docs/apps/openssl.html#PASS_PHRASE_ARGUMENTS
    X509_EXTRA_ARGS = ()

    def openssl(*args):
        cmdline = [OPENSSL] + list(args)
        subprocess.check_call(cmdline)

    def dfile(ext):

        file = os.path.join('domains', '%s.%s' % (domain, ext))

        if (DEBUG):
            print('dfile is: ' + str(file))

        return file

    def gencert(
            domain,
            country_code,
            state_code,
            locality,
            organization_name,
            organizational_unit,
            email,
            rootdir=MYDIR,
            keysize=KEY_SIZE,
            days=DAYS,
            ca_cert=CA_CERT,
            ca_key=CA_KEY):

        ca_cert = 'domains/' + str(ca_cert)
        ca_key = 'domains/' + str(ca_key)

        if (DEBUG):
            print('domain: ' + str(domain))
            print('rootdir: ' + str(rootdir))
            print('keysize: ' + str(keysize))
            print('days: ' + str(days))
            print('ca_cert:' + str(ca_cert))
            print('ca_key: ' + str(ca_key))

        # Changinge to the root directory
        os.chdir(rootdir)

        if not os.path.exists('domains'):

            if(DEBUG):
                print('creating domains directory')

            os.mkdir('domains')

        # create a private key and certificate file using OpenSSL. Create the ca.key
        # file with:

        if not os.path.exists(ca_key):

            if (DEBUG):
                print('ca.key file does not exist.')

            openssl(
                'genrsa',
                '-des3',
                '-out',
                rootdir +
                str('domains/ca.key'),
                str(4096))

        # Then, create the ca.cert file with:

        if not os.path.exists(ca_cert):

            if (DEBUG):
                print('ca.key file does not exist.')

            openssl(
                'req',
                '-new',
                '-x509',
                '-days',
                str(3650),
                '-key',
                rootdir +
                str('domains/ca.key'),
                '-out',
                rootdir +
                str('domains/ca.cert'))

        # Generate the private key if it does not exist
        if not os.path.exists(dfile('key')):

            if (DEBUG):
                print ('generating key file: ' + str(dfile('key')))

            openssl('genrsa', '-out', dfile('key'), str(keysize))

        if (DEBUG):
            print ('opening config file: ' + str(dfile('config')))

        # Creates a domain.config file with the template
        if (DEBUG):
            print("Creating config file")

        config = open(dfile('config'), 'w')
        config.write(
            OPENSSL_CONFIG_TEMPLATE % {
                'domain': domain,
                'country_code': country_code,
                'state_code': state_code,
                'locality': locality,
                'organization_name': organization_name,
                'organizational_unit': organizational_unit,
                'email': email})
        config.close()

        # Creating certificate signing request
        if (DEBUG):
            print('reading: ' + str(dfile('key')))
            print('creating: ' + str(dfile('request')))

        openssl('req', '-new', '-key', dfile('key'), '-out', dfile('request'),
                '-config', dfile('config'))

        if (DEBUG):
            print('reading: ' + str(dfile('request')))
            print('creating: ' + str(dfile('cert')))
            print('domain: ' + str(domain))
            print('rootdir: ' + str(rootdir))
            print('keysize: ' + str(keysize))
            print('days: ' + str(days))
            print('ca_cert:' + str(ca_cert))
            print('ca_key: ' + str(ca_key))

        openssl('x509',
                '-req',
                '-days',
                str(days),
                '-in',
                dfile('request'),
                '-CA',
                str(ca_cert),
                '-CAkey',
                str(ca_key),
                '-set_serial',
                '0x%s' % hashlib.md5(domain + str(datetime.datetime.now())).hexdigest(),
                '-out',
                dfile('cert'),
                '-extensions',
                'v3_req',
                '-extfile',
                dfile('config'),
                *X509_EXTRA_ARGS)

        print("\n")
        print("###############################################################")
        print "Done. The private key is at %s, the cert is at %s, and the CA cert is at %s." % (dfile('key'), dfile('cert'), ca_cert)
        print("###############################################################")

    domain = raw_input("Enter domain name (example: name.com): [ENTER]")

    print("\n")
    print("#########################################################")
    print("Enter information for self signed certificate authority")
    print("#########################################################")
    country_code = raw_input("Enter 2 digit country code. [ENTER]")
    state_code = raw_input("Enter 2 digit state code. [ENTER]")
    locality = raw_input("Enter city name. [ENTER]")
    organization_name = raw_input("Enter organization name. [ENTER]")
    organizational_unit = raw_input("Enter organizational unit name. [ENTER]")
    email = raw_input("Enter email address. [ENTER]")

    gencert(
        domain,
        country_code,
        state_code,
        locality,
        organization_name,
        organizational_unit,
        email)


except (KeyboardInterrupt, SystemExit):
    sys.exit()
