import os
import hashlib
import hmac
from ecdsa import SigningKey, NIST256p
from ecdsa.util import sigencode_der


def sha256(message):
    return hashlib.sha256(message).digest()


def hmac_sha256(key, message):
    return hmac.new(key, message, hashlib.sha256).digest()


def int_to_bytes(n, length):
    return n.to_bytes(length, byteorder='big')


def bits2int(bits, q):
    k = (len(bits) + 7) // 8
    bits_int = int.from_bytes(bits, byteorder='big')
    if bits_int >= q:
        bits_int >>= (8 * k - q.bit_length())
    return bits_int


def bits2octets(bits, q):
    x = bits2int(bits, q)
    k = (q.bit_length() + 7) // 8
    return int_to_bytes(x, k)


def generate_k(msg, private_key):
    q = NIST256p.order
    V = b'\x01' * 32
    K = b'\x00' * 32
    K = hmac_sha256(K + b'\x00' + private_key + msg, V + msg)
    V = hmac_sha256(K, V)
    K = hmac_sha256(K + b'\x01' + private_key + msg, V + msg)
    V = hmac_sha256(K, V)

    while True:
        T = b''
        while len(T) < 32:
            V = hmac_sha256(K, V)
            T += V
        k = bits2int(T, q)
        if k >= 1 and k < q:
            return k
        K = hmac_sha256(K + b'\x00', V)


def generate_random_private_key():
    # Generate a random 256-bit number for the private key
    return os.urandom(32)


def sm2_sign(message, private_key):
    curve = NIST256p.curve
    G = NIST256p.generator
    d = int.from_bytes(private_key, byteorder='big')
    k = generate_k(message, private_key)

    P = d * G
    r = (int(P.x()) + k) % NIST256p.order
    if r == 0:
        raise ValueError("Failed to sign the message. Try again.")

    e = int.from_bytes(sha256(message), byteorder='big')
    s = pow((1 + d) % NIST256p.order, -1, NIST256p.order) * (k - r * d) % NIST256p.order

    # DER encoding of the signature
    signature = sigencode_der(r, s, curve)

    return signature


# Generate a random private key
random_private_key = generate_random_private_key()

# Test example
message = b"Hello, SM2!"
signature = sm2_sign(message, random_private_key)
print("SM2 Signature (DER-encoded):", signature.hex())
