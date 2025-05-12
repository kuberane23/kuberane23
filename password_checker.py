import string
import os
import math
import getpass  # for hiding password input


password = getpass.getpass("Enter your password to check its strength: ")


upper_case = any(c in string.ascii_uppercase for c in password)
lower_case = any(c in string.ascii_lowercase for c in password)
special = any(c in string.punctuation for c in password)
digits = any(c in string.digits for c in password)

characters = [upper_case, lower_case, special, digits]
length = len(password)
score = 0


if os.path.exists('password_list.txt'):
    with open('password_list.txt', 'r') as f:
        common = f.read().splitlines()

    if password in common:
        print("Password was found in a data breach. Score: 0/7")
        exit()
else:
    print("Warning: 'password_list.txt' not found. Skipping breach check.")


if length > 8:
    score += 1
if length > 12:
    score += 1
if length > 16:
    score += 1
if length > 20:
    score += 1

print(f"🔍 Password length is {length}, adding {score} points.")


variety = sum(characters)
if variety > 1:
    score += 1
if variety > 2:
    score += 1
if variety > 3:
    score += 1

print(f" Password has {variety} different character types, adding {variety - 1} points.")


pool_size = 0
if upper_case: pool_size += 26
if lower_case: pool_size += 26
if digits: pool_size += 10
if special: pool_size += len(string.punctuation)
entropy = math.log2(pool_size ** length) if pool_size else 0
print(f"🔒 Estimated entropy: {entropy:.2f} bits")


print(f"Final Score: {score} / 7")
if score < 4:
    print("The password is quite weak!")
elif score == 4:
    print("The password is okay.")
elif 4 < score < 6:
    print("The password is pretty good.")
elif score >= 6:
    print("The password is strong!")


if score < 7:
    print("\nSuggestions to improve your password:")
    if length <= 12:
        print("- Make your password longer.")
    if not upper_case:
        print("- Add some uppercase letters.")
    if not lower_case:
        print("- Add some lowercase letters.")
    if not digits:
        print("- Include numbers.")
    if not special:
        print("- Add special characters (e.g. !@#$).")
