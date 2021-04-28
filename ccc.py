#!/usr/bin/env python3

import OpenSSL, ssl, socket
from datetime import datetime
from sys import argv
try:
    hostname = argv[1]
except:
    hostname = 'example.com'
try:
    port = int(argv[2])
except:
    port = 443

#Creating a context. We don't care about cert issuer trust or hostname matching
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:

            der_cert = sslsock.getpeercert(True)
            pem_cert = ssl.DER_cert_to_PEM_cert(der_cert)
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
            
            cert_expire_date_as_string = x509.get_notAfter().decode('ascii')
            cert_issue_date_as_string = x509.get_notBefore().decode('ascii')
            cert_issuer = x509.get_issuer().CN
            now = datetime.now()
            cert_expire_date = datetime.strptime(cert_expire_date_as_string, '%Y%m%d%H%M%SZ')
            cert_issue_date = datetime.strptime(cert_issue_date_as_string, '%Y%m%d%H%M%SZ')
            days_left = (cert_expire_date - now).days
            ipaddr = socket.gethostbyname(hostname)
            
except ConnectionRefusedError:
    print(f"{hostname}:{port} - ERROR: Connection refused.")
except socket.gaierror:
    print(f"{hostname} - ERROR: Name resolution failure.")
except Exception as e:
    print(f"ERROR - {e}.")
else:
    print(f"{hostname}:{port} ({ipaddr}):  \nIssuer: {cert_issuer}\nIssued: {cert_issue_date}\nExpires: {cert_expire_date}\n{days_left} days remaining.\n")




