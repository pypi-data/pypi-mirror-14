#!/usr/bin/env python

import boto3.session
from aws_cli_menu_helper import *
import sys
import os
import hashlib
import subprocess
import datetime
import re


try:

    profile_name = get_profile_name()
    print("\n\n")

    session = boto3.session.Session(profile_name=profile_name)

    client = session.client('iam')

    print("\n")
    print("###################################################")
    print("Before you upload the certificate, you need to ")
    print("create it using Main Menu > IAM > Server Certificates > Create Server Certificate")
    print("###################################################")
    print("\n")

    directory = raw_input(
        "Enter directory with certificates (example: /tmp). [ENTER]")

    menu = {}
    counter = 0
    for dirname, dirnames, filenames in os.walk(directory):

        for filename in filenames:
            counter += 1
            menu[counter] = os.path.join(dirname, filename)

    print "\n\n"
    print '#########################################'
    print '## Select Certificate                  ##'
    print '#########################################'
    for key in sorted(menu):
        print str(key) + ":" + menu[key]

    pattern = r'^[0-9]+$'
    while True:
        ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
        if re.match(pattern, ans) is not None:
            if int(ans) in menu:
                cert = menu[int(ans)]
                break

    if not os.path.exists(cert):
        print("\n")
        print("##############################################")
        print("The cert does not exist...please try again.")
        print("##############################################")

    else:

        cert_txt = subprocess.check_output(
            ["openssl", "x509", "-outform", "PEM", "-in", cert])

        cert_txt = cert_txt.lstrip()
        cert_txt = cert_txt.rstrip()

        print "\n\n"
        print '#########################################'
        print '## Select Private Key                  ##'
        print '#########################################'
        for key in sorted(menu):
            print str(key) + ":" + menu[key]

        pattern = r'^[0-9]+$'
        while True:
            ans = raw_input("Make A Choice: [ENTER](Cntrl-C to exit)")
            if re.match(pattern, ans) is not None:
                if int(ans) in menu:
                    private_key = menu[int(ans)]
                    break

        if not os.path.exists(private_key):
            print("\n")
            print("######################################################")
            print("The private key does not exist...please try again.")
            print("######################################################")

            # Need to add the ability for certificate chaining

        else:

            key_txt = subprocess.check_output(
                ["openssl", "rsa", "-in", private_key, '-outform', 'PEM'])

            key_txt = key_txt.lstrip()
            key_txt = key_txt.rstrip()

            print(key_txt)

            print("\n")
            cert_name = raw_input(
                "Enter name for this server certificate. [ENTER]")

            response = client.upload_server_certificate(
                Path='/',
                ServerCertificateName=cert_name,
                CertificateBody=cert_txt,
                PrivateKey=key_txt
                #    CertificateChain='string'
            )

            print("\n")
            print(pretty(response))

except (KeyboardInterrupt, SystemExit):
    sys.exit()
