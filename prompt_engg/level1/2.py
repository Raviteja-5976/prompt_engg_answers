# 2. Write a program function that counts the number of uppercase and 
# lowercase letters in a given string.


def count_cases(text):
  """
  Counts the number of uppercase and lowercase letters in a string.

  Args:
    text: The string to analyze.

  Returns:
    A dictionary with keys 'uppercase' and 'lowercase', and their respective counts.
  """

  uppercase = 0
  lowercase = 0

  for char in text:
    if char.isupper():
      uppercase += 1
    elif char.islower():
      lowercase += 1

  return {'uppercase': uppercase, 'lowercase': lowercase}

# Example usage
text = input()
counts = count_cases(text)

print("Uppercase letters:", counts['uppercase'])
print("Lowercase letters:", counts['lowercase'])
