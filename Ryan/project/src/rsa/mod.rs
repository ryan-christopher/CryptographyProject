// import for random number generator
use rand::Rng;

// miller_rabin used to test if a number is prime or not, takes as input the
// number to be tested for primality and the number of tests to occur
pub fn miller_rabin(n: i128, num_tests: i32) -> bool {
    if n % 2 == 0 {
        return false;
    }

    // create variables for m and r
    let mut m = n - 1;
    let mut r = 0;
    
    // calculate r and m where n - 1 = (2 ** r) * m
    while m % 2 == 0 {
        m = m / 2;
        r += 1;
    }
    
    //println!("n: {:?}\nm: {:?}, r: {:?}", n, m, r);

    // create vector to check if b generated was a repeat or not
    let mut b_values = Vec::<i128>::new();

    for mut _x in 1..=num_tests {
        // generate random value b between 1 and n
        let b = rand::rng().random_range(1..n);

        // if b was already generated, iterate again to choose another random value
        if b_values.contains(&b){
            _x -= 1;
            println!("b value repeated, choosing again");
        }
        
        else{
            b_values.push(b);
            // b**m mod n
            let test_1 = fast_exponentiation(b, m, n);
            if test_1 == 1 || test_1 == n - 1 {
                continue;
            }
            // (b**m)**2 mod n
            let b_second_test = fast_exponentiation(test_1, 2, n);
            let test_2 = fast_exponentiation(b_second_test, m, n);
            if test_2 == n - 1 {
                continue;
            }
            // ((b**m)**2)**2 mod n
            let b_third_test = fast_exponentiation(test_2, 2, n);
            let test_3 = fast_exponentiation(b_third_test, m, n);
            if test_3 == n - 1 {
                continue;
            }
            // ((b**m)**2)**r-1 mod n
            let b_fourth_test = fast_exponentiation(test_2, r - 1, n);
            let test_4 = fast_exponentiation(b_fourth_test, m, n);
            if test_4 == n - 1 {
                continue;
            }
            else{
                // if this point is reached, the number is not prime
                return false;
            }
        }
    }
    println!("p: {:?}", n);

    return true;
}



// fast_exponentation takes i128 values for x, e, and n
// and calculates (x**e) mod n, returns value as y
pub fn fast_exponentiation(mut x: i128, mut e: i128, n: i128) -> i128 {
    // set y to default value of 1
    let mut y = 1;

    // continue until value is 0
    while e > 0 {
        // if e is even, the ending binary digit is 0, divide e
        // by 2 and raise x by power of 2
        if e % 2 == 0 {
            e = e / 2;
            x = x.pow(2) % n;
        }
        // if e is odd, subtract 1 from e, multiply y by x,
        // and get the product mod n
        else {
            e -= 1;
            y = (x * y) % n;
        }
    }
    //println!("x: {:?}, e: {:?}, y: {:?}", x, e, y);
    // return y when done
    return y;
}

// random_prime takes a minimum and maximum value as input, then finds
// a prime number within that range
pub fn random_prime(min_val: i128, max_val: i128) -> i128 {
    let mut prime_found = false;
    let mut number: i128 = 0;

    while prime_found != true {
        // randomly choose a value within the range min_val to max_val
        number = rand::rng().random_range(min_val..=max_val);
        // perform miller-rabin test with 20 attempts, if it is true then
        // a prime has been found
        if miller_rabin(number, 20) {
            prime_found = true;
        }
    }
    return number;
}

pub fn euclid(val_1: i128, val_2: i128) -> i128 {
    let x;
    let y;
    // determine larger value
    if val_1 > val_2 {
        x = val_1;
        y = val_2;
    } else {
        x = val_2;
        y = val_1;
    }
    // calculate modulo
    let z = x % y;
    // recursively call the function until the value of z is 0 or 1
    // indicating that the gcd has been found
    if z == 0 {
        //println!("m: {:?}, n: {:?}, z: {:?}", x, y, z);
        //println!("gcd: {:?}", y);
        return y
    } else if z == 1 {
        //println!("m: {:?}, n: {:?}, z: {:?}", x, y, z);
        //println!("gcd: {:?}", z);
        return z
    } else {
        //println!("m: {:?}, n: {:?}, z: {:?}", x, y, z);
        return euclid(y, z);
    }
}

pub fn extended_euclid(a: i128, b: i128) -> (i128, i128) {
    //Base case
    if a ==0 { 
        return (0, 1)
    }
    
    //recursive step(traversing down)
    let (x1,y1) = extended_euclid(b%a, a);   
    
    //calculating n and m at each step back up
    let n = y1 - (b/a) * x1;
    let m = x1;
    
    return (n, m);
}

pub fn find_inverse(val_1: i128, val_2: i128) -> i128 {
    let (mut x, y) = extended_euclid(val_1, val_2);

    while x < 0 {
        x += val_2;
    }

    return x;
}

pub fn generate_pqn(min_val: i128, max_val: i128) -> (i128, i128, i128, i128) {
    let p = random_prime(min_val, max_val);
    let q = random_prime(min_val, max_val);
    return (p, q, p * q, (p - 1) * (q - 1))
}

pub fn find_encryption_component(n: i128) -> i128 {
    loop {
        let number = rand::rng().random_range(1..=n - 1);
        if euclid(number, n) == 1 {
            return number
        }
    }
}

pub fn encrypt(message: i128, e: i128, n: i128) -> i128 {
    return fast_exponentiation(message, e, n)
}

pub fn decrypt(ciphertext: i128, n: i128, d: i128) -> i128 {
    return fast_exponentiation(ciphertext, d, n)
}