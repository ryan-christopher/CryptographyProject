mod elgamal;
mod rsa;
use rand::Rng;
fn main() {
    // random_prime has been tested up to 10,000,000,000,000,000,000
    // ========== EL GAMAL ==========
    //let prime = elgamal::random_prime(1000, 10000);
    //let generator = elgamal::find_rand_primitive_root(prime);
    //let r = rand::rng().random_range(1..prime);
    //let pub_key = elgamal::elgamal_gen_public_key(prime, generator, r);
    //println!("Prime: {}\nGenerator: {}\nr: {}\nPublic Key: {}", prime, generator, r, pub_key);
    //let decrypted_message = elgamal::decrypt(5343, 1768, 1018, 5639);
    //println!("{}", decrypted_message);
    //let r = rand::rng().random_range(1..9871);
    //let pub_key = elgamal_gen_public_key(9871, 3, r);
    //let message = 617 as i128;
    //let encrypted_message = elgamal::encrypt(message, 3124, r, 9871);
    //println!("Public key: {}\nEncrypted message: {}\nr: {}", pub_key, encrypted_message, r);
    //let intercepted_message = elgamal::intercept(169, 2, 718, 255, 787);
    //println!("Intercepted message: {}", intercepted_message);
     
    // ==========   RSA    ==========
    //let (p, q, n, phi_n) = rsa::generate_pqn(1000, 10000);
    //println!("p: {}, q: {}, n: {}, phi_n: {}", p, q, n, phi_n);
    //let e = rsa::find_encryption_component(phi_n);
    //println!("encryption component: {}", e);
    //let d = rsa::find_inverse(e, phi_n);
    //println!("d: {}", d);
    //let encrypted_message = rsa::encrypt(9878, 65537, 73846469);
    //println!("encrypted message: {}", encrypted_message);
    //let decrypted_message = rsa::decrypt(7510948, 25931089, 25700683);
    //println!("decrypted message: {}", decrypted_message);
    println!("{}", rsa::intercept(12674548, 18865541, 65537));

}
