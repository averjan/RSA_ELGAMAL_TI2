# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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


def are_relatively_prime(a, b):
    for i in range(2, min(a, b) + 1):
        if a & i == b % i == 0:
            return False
    return True


def euclide(a, b):
    d0, d1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while d1 > 1:
        q = d0 // d1
        d2 = d0 % d1
        x2 = x0 - (q * x1)
        y2 = y0 - (q * y1)
        d0, d1 = d1, d2
        x0, x1 = x1, x2
        y0, y1 = y1, y2

    return x1, y1, d1


def create_key_pair():
    p = int(input("Enter p value: "))
    q = int(input("Enter q value: "))
    r = p * q
    x = (p - 1) * (q - 1)
    for e in range(3, x, 2):
        if are_relatively_prime(e, x):
            break

    # for d in range(3, x, 2):
    #     if d * e % x == 1:
    #         break

    temp_x, d, nod = euclide(x, e)
    if d < 0:
        d += x

    return (e, r), (d, r)


def encrypt(key, message):
    encrypted_message = ""
    for m in message:
        encrypted_message += chr(pow(ord(m) - ord('A'), key[0], key[1])
                                 + ord('A'))

    return encrypted_message


def decrypt(key, text):
    original_message = ""
    for m in text:
        original_message += chr(pow(ord(m) - ord('A'), key[0], key[1])
                                + ord('A'))

    return original_message


# Main Prog

public_key, private_key = create_key_pair()
msg = input("Enter the message: ")
encrypted_msg = encrypt(public_key, msg)
print(encrypted_msg)
original_msg = decrypt(private_key, encrypted_msg)
print(original_msg)
