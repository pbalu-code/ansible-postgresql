#!/bin/bash

openssl req -new -nodes -text -out root.csr \
  -keyout root.key -subj "/CN=root.local"

chmod og-rwx root.key

#Then, sign the request with the key to create a root certificate authority (using the default OpenSSL configuration file location on Linux):

openssl x509 -req -in root.csr -text -days 3650 \
  -extfile /etc/ssl/openssl.cnf -extensions v3_ca \
  -signkey root.key -out root.crt

#Finally, create a server certificate signed by the new root certificate authority:

openssl req -new -nodes -text -out pgmaster.csr \
  -keyout pgmaster.key -subj "/CN=postgresql.local"


openssl x509 -req -in pgmaster.csr -text -days 365 \
  -CA root.crt -CAkey root.key -CAcreateserial \
  -out pgmaster.crt
