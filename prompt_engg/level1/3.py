# 3. Write a program that generates a random password with 8 characters, 
# containing at least one uppercase letter, one lowercase letter, one digit, 
# and one special symbol.

import random
import string

def generate_password():
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_symbols = string.punctuation
    
    # Initialize an empty list to store the password characters
    password = []
    
    # Add at least one character from each character set
    password.append(random.choice(lowercase_letters))
    password.append(random.choice(uppercase_letters))
    password.append(random.choice(digits))
    password.append(random.choice(special_symbols))
    
    # Fill up the rest of the password with random characters
    for _ in range(4):
        password.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    # Convert the list of characters into a string
    return ''.join(password)

# Generate and print the password
print("Generated Password:", generate_password())
