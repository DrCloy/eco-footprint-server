from hashlib import sha256


def verifySignature(message, secret, signature):
    return sha256((message + '_' + secret).encode()).hexdigest() == signature
