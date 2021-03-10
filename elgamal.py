import math
import random


class PublicKey:
    def __init__(self, p, g, y):
        self.p = p
        self.g = g
        self.y = y


class PrivateKey:
    def __init__(self, p, x):
        self.p = p
        self.x = x


def are_relatively_prime(a, b):
    for i in range(2, min(a, b) + 1):
        if a & i == b % i == 0:
            return False
    return True


def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n / 2

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n / i

    if n > 2:
        factors.append(n)

    return factors


def find_primitive_root(p, primes):
    g = random.randint(2, p - 1)
    for i in primes:
        if pow(g, (p - 1) / i) % p == 1:
            return find_primitive_root(p, primes)

    return g


def create_key_pair():
    p = int(input("Enter the p value: "))
    primes = prime_factors(p)
    g = find_primitive_root(p, primes)
    x = random.randrange(p - 1)
    y = pow(g, x, p)
    return PublicKey(p, g, y), PrivateKey(x, p)


def encrypt(key, message):
    k = random.randrange(2, key.p - 1)
    while not are_relatively_prime(key.p - 1, k):
        k = random.randrange(2, key.p - 1)

    encrypt_message = []
    for m in message:
        k = random.randrange(2, key.p - 1)
        while not are_relatively_prime(key.p - 1, k):
            k = random.randrange(2, key.p - 1)

        a = pow(key.g, k, key.p)
        b = (pow(key.y, k) * (ord(m) - ord('A'))) % key.p
        encrypt_message.extend([a, b])

    return encrypt_message


def decrypt(key, cipher):
    # decrpyts each pair and adds the decrypted integer to list of plaintext integers
    plaintext = []

    # cipherArray = cipher.split()
    if not len(cipher) % 2 == 0:
        return "Malformed Cipher Text"
    for i in range(0, len(cipher), 2):
        # c = first number in pair
        a = int(cipher[i])
        # d = second number in pair
        b = int(cipher[i + 1])

        # s = c^x mod p
        s = pow(a, key.x, key.p)
        # plaintext integer = ds^-1 mod p
        plain = (b * pow(s, key.p - 2, key.p)) % key.p
        # add plain to list of plaintext integers
        plaintext.append(plain)

    # decryptedText = decode(plaintext, key.iNumBits)
    decrypted_text = ""
    for m in plaintext:
        decrypted_text += chr(m + ord('A'))

    # remove trailing null bytes
    decrypted_text = "".join([ch for ch in decrypted_text if ch != '\x00'])

    return decrypted_text


def decrypt2(key, message, p):
    original_message = ""
    it = iter(message)
    for a in it:
        original_message += chr(((next(it) * pow(a, - key)) % p) + ord('A'))

    return original_message


# Main Prog

msg = input("Enter the message: ")
public_key, private_key = create_key_pair()
encrypted_message = encrypt(public_key, msg)
print(encrypted_message, sep=" ")
original_message = decrypt(private_key, encrypted_message)
print(original_message)
