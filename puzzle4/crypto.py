import hashlib
import ed25519

def generate_keys():
    # Heh, I can use private and public so freely in Python.
    private, public = ed25519.create_keypair()

    return (private.to_ascii(encoding="hex"),
            public.to_ascii(encoding="hex"))

def sign(message, private):
    signing_key = ed25519.SigningKey(str(private), encoding="hex")
    return signing_key.sign(str(message), encoding="base64")

def verify(message, public, signature):
    try:
        vk = ed25519.VerifyingKey(str(public), encoding="hex")

        vk.verify(str(signature),
                  str(message),
                  encoding="base64")

        return True
    except ed25519.BadSignatureError:
        return False