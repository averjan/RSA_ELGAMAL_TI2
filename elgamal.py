import math
import random


def is_prime(num):
    if num > 1:
        for i in range(2, num):
            if num % i == 0:
                return False

    return True


def fast_exp(a, z, n):
    a1 = a
    z1 = z
    x = 1
    while z1 != 0:
        while z1 % 2 == 0:
            z1 //= 2
            a1 = (a1 * a1) % n

        z1 -= 1
        x = (x * a1) % n

    return x


class PublicKey:
    def __init__(self, p, g, y):
        self.p = p
        self.g = g
        self.y = y


class PrivateKey:
    def __init__(self, x, p):
        self.p = p
        self.x = x


def are_relatively_prime(a, b):
    for i in range(2, min(a, b) + 1):
        if (a % i == 0) and (b % i == 0):
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
        if fast_exp(g, (p - 1) / i, p) == 1:
            return find_primitive_root(p, primes)

    return g


def need_more_size(msg, r):
    alphabet_start = ord(' ')
    for m in msg:
        if ord(m) - alphabet_start >= r:
            print("Message requires key longer")
            return True

    return False


def get_p():
    p = int(input("Enter the p value: "))
    while not is_prime(p):
        p = int(input("Enter the p value: "))

    return p


def create_key_pair(msg):
    p = get_p()
    while need_more_size(msg, p):
        p = get_p()

    primes = prime_factors(p - 1)
    g = find_primitive_root(p, primes)
    x = random.randrange(p - 1)
    y = fast_exp(g, x, p)
    return PublicKey(p, g, y), PrivateKey(x, p)


def encrypt(key, message):
    alphabet_start = ord(' ')
    encrypt_list = []
    encrypt_message = ""
    for m in message:
        k = random.randrange(2, key.p - 1)
        while not are_relatively_prime(key.p - 1, k):
            k = random.randrange(2, key.p - 1)

        a = fast_exp(key.g, k, key.p)
        b = (pow(key.y, k) * (ord(m) - alphabet_start)) % key.p
        encrypt_list.extend([a, b])
        encrypt_message += chr(a + alphabet_start) + chr(b + alphabet_start)

    return encrypt_list, encrypt_message


def decrypt(key, message):
    original = ""
    it = iter(message)
    phi = key.p - 2
    for a in it:
        b = next(it)
        original += chr(((b * pow(a, key.x * phi)) % key.p) + ord(' '))

    return original


# Main Prog

msg = input("Enter the message: ")
public_key, private_key = create_key_pair(msg)
encrypted, encrypted_message = encrypt(public_key, msg)
print(encrypted_message)
original_message = decrypt(private_key, encrypted)
print(original_message)
