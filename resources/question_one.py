def solution(i):


  # Determine prime sequence
  primes = getPrimeNumbers()

  return primes[i:i + 5]


def getPrimeNumbers():
  '''Returns the string of prime
  numbers up to 10k+5 positions.'''

  s = ''
  prime = 2
  while len(s) < 10005:

    # Add new prime to s
    s += str(prime)

    # Calculate next prime
    prime += 1
    while not is_prime(prime):
      prime += 1

  return s


def is_prime(n):
  '''Tests if a number is prime. '''
  for i in range(2, n):
    if n % i == 0:
      return False
  return True


print(solution(0))
# 23571
print(solution(3))
# 71113