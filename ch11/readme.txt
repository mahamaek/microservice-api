# command to generate private/public key pair with certiictation following x.509 standard to bind a pulbic key to an identity
# this produces a private key and public CERTIFICATE


openssl req -x509 -nodes -newkey rsa:2048 -keyout private_key.pem -out public_key.pem -subj "/CN=coffeemesh"


# To obtain the public key from the public CERTIFICATE, 

openssl x509 -pubkey -noout < public_key.pem > pubkey.perm


# Decode jwt token
1. using jwt.io or jwt.ms

2. using base64 decoding on terminal

echo eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9| base64 --decode

3. We can also use python base64 library
