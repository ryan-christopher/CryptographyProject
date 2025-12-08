from random import randint
import math


def fastExponentiation(x, e, n):
    y = 1

    while e > 0:
        if e % 2 == 0:
            e = e / 2
            x = (x ** 2) % n
        else:
            e -= 1
            y = (x * y) % n
    
    return y


def millerRabin(n, num_tests):
    if n % 2 == 0:
        return False
    
    m = n - 1
    r = 0

    while m % 2 == 0:
        m = m / 2
        r += 1

    b_values = []

    for x in range(1, num_tests):
        b = randint(1, n)
        if b in b_values:
            x -= 1
            print("b value repeated, choosing again")
        else:
            b_values.append(b)
            test1 = fastExponentiation(b, m, n)
            if test1 == 1 or test1 == n - 1:
                return True
            b2 = fastExponentiation(test1, 2, n)
            test2 = fastExponentiation(b2, m, n)
            if test2 == n - 1:
                return True
            b3 = fastExponentiation(test2, 2, n)
            test3 = fastExponentiation(b3, m, n)
            if test3 == n - 1:
                return True
            b4 = fastExponentiation(test2, r - 1, n)
            test4 = fastExponentiation(b4, m, n)
            if test4 == n - 1:
                return True
            
            return False
    return True



def randomPrime(minVal, maxVal): 
    primeFound = False
    number = 0

    while primeFound != True:
        number = randint(minVal, maxVal)
        if millerRabin(number, 20):
            primeFound = True

    return number


def isPrime(n):
    if n % 2 == 0:
        return False
    if n == 3:
        return True
    searchVal = 3
    maxVal = math.ceil(math.sqrt(n)) + 1
    while searchVal <= maxVal:
        if n % searchVal == 0:
            return False
        searchVal += 2

    return True


def getPrimeFactors(p):
    primeFactors = []
    x = p - 1
    if x % 2 == 0:
        primeFactors.append(2)
    i = 3
    while i <= math.ciel(math.sqrt(x)):
        if isPrime(i) and x % i == 0:
            primeFactors.append(i)
        i += 2
    return primeFactors


def isPrimitiveRoot(p, b):
    primeFactors = getPrimeFactors(p)
    for factor in primeFactors:
        if fastExponentiation(b, (p - 1) / factor, p) == 1:
            return False
    return True


def findPrimitiveRoot(p):
    for b in range(2, p):
        if isPrimitiveRoot(p, b):
            return b
    
    return 0
    

def findInverse(val1, val2):
    return fastExponentiation(val1, val2 - 2, val2)


def babyStepGiantStep(logBase, logVal, z):
    m = math.ceil(math.sqrt(z - 1))

    jList = []
    for j in range(0, m):
        jList.append((logBase ** j) % z)

    inverse = findInverse(logBase, z)
    inversePowM = fastExponentiation(inverse, m, z)
    #print(jList)
    iList = []
    for i in range(0, m):
        inversePowMI = fastExponentiation(inversePowM, i, z)
        iList.append((logVal * inversePowMI) % z)
        #print((logVal * inversePowMI) % z)
        if (logVal * inversePowMI) % z in jList:
            return i * m + jList.index((logVal * inversePowMI) % z)
    return 0


def elgamalPublicKey(p, g, r):
    return fastExponentiation(g, r, p)


def encrypt(message, recipientPubKey, privKey, p):
    return message * fastExponentiation(recipientPubKey, privKey, p) % p


def decrypt(cipher, recipientPubKey, r, p):
    inverseVal = fastExponentiation(recipientPubKey, r, p)
    inverse = findInverse(inverseVal, p)
    message = (inverse * cipher) % p
    return message


def intercept(cipher, generator, targetPubKey, recipientPubKey, p):
    recoveredKey = babyStepGiantStep(generator, targetPubKey, p)
    #recoveredKey = babyStepGiantStep(2, 3, 29)
    print("recovered key", recoveredKey)
    message = decrypt(cipher, recipientPubKey, recoveredKey, p)
    return message



#pubKey = elgamalPublicKey(9871, 3, 6767)

#message = 543

#encrypted = encrypt(message, 3124, 6767, 9871)

#print(pubKey, message, encrypted)
# 6854 543 635


pubKey = elgamalPublicKey(8971, 2, 101)

message = 6767 

encrypted = encrypt(message, 2580, 101, 8971)

print(pubKey)

print(encrypted)

decrypted = decrypt(3921, 5563, 4701, 8971)

print(decrypted)

intercepted = intercept(3921, 2, 5563, 2580, 8971)

print(intercepted)