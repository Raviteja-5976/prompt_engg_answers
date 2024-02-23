# 1. Generate a program function that takes a number as input and returns 
# True if it's a prime number, False otherwise. 

def is_prime(n):
  """
  This function checks if a number is prime.

  Args:
    n: The number to check.

  Returns:
    True if n is prime, False otherwise.
  """

  if n <= 1:  # 1 or less is not prime
    return False
  if n <= 3:  # 2 and 3 are prime
    return True
  if n % 2 == 0 or n % 3 == 0:  # Check for divisibility by 2 or 3
    return False

  i = 5
  while i * i <= n:  # Efficiently check divisibility up to the square root of n
    if n % i == 0 or n % (i + 2) == 0:
      return False
    i += 6

  return True

number = int(input("Enter a number: "))
if is_prime(number):
    print(number, "is a prime number")
else:
    print(number, "is not a prime number")
