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

pub fn is_prime(n: i128) -> bool {
    if n % 2 == 0 {
        return false;
    }
    if n == 3 {
        return true;
    }
    let mut search_val = 3 as i128;
    let max_val = ((n as f64).sqrt().ceil() as i128) + 1;
    while search_val <= max_val {
        if n % search_val == 0 {
            return false;
        }
        search_val += 2;
    }
    return true;
}

pub fn get_prime_factors(p: i128) -> Vec<i128> {
    // create vector to check if b generated was a repeat or not
    let mut prime_factors = Vec::<i128>::new();

    let x = p - 1;

    if x % 2 == 0 {
        prime_factors.push(2);
    }
    let mut i = 3;
    while i <= (x as f64).sqrt().ceil() as i128 {
        if is_prime(i) && x % i == 0 {
            prime_factors.push(i);
        }
        i += 2;
    }

    return prime_factors;
}

pub fn is_primitive_root(p: i128, b: i128) -> bool{
    let prime_factors = get_prime_factors(p);

    for factor in prime_factors{
        if fast_exponentiation(b, (p - 1) / factor, p) == 1 {
            return false;
        }
    }

    return true;
}

pub fn find_primitive_root(p: i128) -> i128 {

    for b in 2..p {
        if is_primitive_root(p, b) {
            return b;
        };
    }

    return 0;
}

pub fn find_rand_primitive_root(p: i128) -> i128 {

    let mut counter = 0; 

    while counter < p {
        let b = rand::rng().random_range(2..=p);
        if is_primitive_root(p, b) {
            return b;
        };
        counter += 1;
    }

    return 0;
}


pub fn find_inverse(val_1: i128, val_2: i128) -> i128 {
    return fast_exponentiation(val_1, val_2 - 2, val_2);
}


pub fn elgamal_gen_public_key(p: i128, g: i128, r: i128) -> i128{
    return fast_exponentiation(g, r, p);
}

pub fn elgamal_encrypt(message: i128, recipient_pub_key: i128, priv_key: i128, p: i128) -> i128 {
    let cipher = message * fast_exponentiation(recipient_pub_key, priv_key, p) % p;
    return cipher;
}

pub fn elgamal_decrypt(cipher: i128, recipient_pub_key: i128, r: i128, p: i128) -> i128 {
    //let mut key = fast_exponentiation(recipient_pub_key, priv_key, p);
    let inverse_val = fast_exponentiation(recipient_pub_key, r, p);
    let inverse  = find_inverse(inverse_val, p);
    //println!("{}, {}", inverse, cipher);
    let message = (inverse * cipher) % p;
    return message;
}

pub fn elgamal_intercept(cipher: i128, generator: i128, target_pub_key: i128, recipient_pub_key: i128, p: i128) -> i128 {
    let recovered_key = baby_step_giant_step(generator, target_pub_key, p);
    //println!("{}", recovered_key);
    let message = elgamal_decrypt(cipher, recipient_pub_key, recovered_key, p);
    //println!("{}", message);
    return message
}


// baby_step_giant_step takes the variables log_base, log_val, and z
// as input and finds the discrete log (the value to raise the log_base
// to in order to get log_val mod z)
pub fn baby_step_giant_step(log_base: i128, log_val: i128, z: i128) -> i128 {
    // find m by taking the cieling of the square root of z-1
    let m = (z as f64 - 1.0).sqrt().ceil() as i128;

    // create vector to store list of values for j, then
    // calculate each value for j from 0 to m-1 as (log_base^j) mod z
    let mut j_list = Vec::<i128>::new();
    for j in 0..m {
        j_list.push(log_base.pow(j as u32) % z);
    }

    // create vector to store list of values for i
    // [giving up here, has something to do with multiplicative inverse, use extended euclidian algo and if it is 1 do something?]
    //println!("m: {}", m);
    //println!("j: {:?}", j_list);
    let inverse = find_inverse(log_base, z);
    let inverse_pow_m = fast_exponentiation(inverse, m, z);

    let mut i_list = Vec::<i128>::new();
    for i in 0..m {
        let inverse_pow_m_i = fast_exponentiation(inverse_pow_m, i, z);
        i_list.push((log_val * inverse_pow_m_i)  % z);

        let check_i_and_m = j_list.clone().into_iter().position(|x| x == i_list[i as usize]);
        if check_i_and_m.is_some(){
            //println!("{}", i_list[i as usize]);
            //println!("{}", i * m + check_i_and_m.unwrap() as i128);
            return i * m + check_i_and_m.unwrap() as i128;
        }

    }
    return 0;
}