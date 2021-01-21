## Server keys

Create a self-signed certificate for your server.

Not recommended for a production environment!

### Self-signed certificate

Create a certificate in the TLS certificate directory, as `root`:

    cd /etc/pki/tls/certs/
    openssl genrsa -aes128 2048 > server.key
	
Remove the passphrase from the private key:

    openssl rsa -in server.key -out server.key
    openssl req -utf8 -new -key bm.key -out server.csr

Create certificate with 10 years expiration date:

    openssl x509 -in server.csr -out server.crt -req -signkey server.key -days 3650
    mv server.key /etc/pki/tls/private

### SELinux

Make sure the `SELinux` settings are correct:

    restorecon /etc/pki/tls/certs/server.crt
    restorecon /etc/pli/tls/private/server.key
    chmod 600 server.key

