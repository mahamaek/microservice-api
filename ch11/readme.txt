# command to generate private/public key pair with certiictation following x.509 standard to bind a pulbic key to an identity

openssl req -x509 -nodes -newkey rsa:2048 -keyout private_key.pem -out public_key.pem -subj "/CN=coffeemesh"