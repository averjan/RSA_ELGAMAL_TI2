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


def are_relatively_prime(a, b):
    for i in range(2, min(a, b) + 1):
        if (a % i == 0) and (b % i == 0):
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


def need_more_size(msg, r):
    alphabet_start = ord(' ')
    for m in msg:
        if ord(m) - alphabet_start >= r:
            print("Message requires key longer")
            return True

    return False


def get_pq():
    p = q = 0
    while p == q:
        p = int(input("Enter p value: "))
        while not is_prime(p):
            print("p must be prime")
            p = int(input("Enter p value: "))

        q = int(input("Enter q value: "))
        while not is_prime(q):
            print("p must be prime")
            q = int(input("Enter q value: "))

    return p, q


def create_key_pair(msg):
    p, q = get_pq()
    r = p * q
    while need_more_size(msg, r):
        p, q = get_pq()
        r = p * q

    x = (p - 1) * (q - 1)
    e = 2
    for i in range(3, x, 2):
        if are_relatively_prime(i, x):
            e = i
            break

    temp_x, d, nod = euclide(x, e)
    if d < 0:
        d += x

    return (e, r), (d, r)


# def encrypt(key, message):
#     encrypted_message = ""
#     for m in message:
#         encrypted_message += chr(pow(ord(m) - ord('A'), key[0], key[1])
#                                  + ord('A'))
#
#     return encrypted_message


# def decrypt(key, text):
#     original_message = ""
#     for m in text:
#         original_message += chr(pow(ord(m) - ord('A'), key[0], key[1])
#                                 + ord('A'))
#
#     return original_message


def encrypt(key, message):
    encrypted_list = []
    encrypted_message = ""
    alphabet_start = ord(' ')
    for m in message:
        c = fast_exp(ord(m) - alphabet_start, key[0], key[1])
        encrypted_list.append(c)
        encrypted_message += chr(c + alphabet_start)

    return encrypted_list, encrypted_message


def decrypt(key, text):
    original_list = []
    original_message = ""
    alphabet_start = ord(' ')
    for c in text:
        m = fast_exp(c, key[0], key[1]) + alphabet_start
        original_list.append(m)
        original_message += chr(m)

    return original_list, original_message


# Main Prog

msg = input("Enter the message: ")
public_key, private_key = create_key_pair(msg)
encrypted_lst, encrypted_msg = encrypt(public_key, msg)
print(encrypted_msg)
original_lst, original_msg = decrypt(private_key, encrypted_lst)
print(original_msg)
