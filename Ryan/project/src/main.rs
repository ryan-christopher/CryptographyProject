//mod elgamal;
mod rsa;
fn main() {
    // random_prime has been tested up to 10,000,000,000,000,000,000
    //println!("{:?}", random_prime(1, 1000000000000));
/* 
    // Alexan provides p and g
    // Ryan chooses a random number (r) as a private key and calculates the public key
    println!("Ryan's public key: {:?}", elgamal_gen_public_key(5393, 3, 120));
    // Alexan sends Ryan the encrypted message along with g^l where l is the nonce
    println!("public val = 4525");
    println!("Ciphertext = 393");
    // Ryan decrypts with the ciphertext, g^nonce mod p, Ryan's private key, and p
    println!("Message decrypted: {:?}", elgamal_decrypt(3940, 743, 120, 5393));
    println!("public val: {:?}", elgamal_gen_public_key(3677, 3, 120));
    */
    // EL GAMAL TEST RUN
    /* 
    println!("p = 3677");
    println!("primitive root = {}", elgamal::find_primitive_root(3677));
    println!("my public val: 683");
    println!("decrypted: {}", elgamal::elgamal_decrypt(1942, 2341, 1234, 3677));
    println!("encrypted: {}", elgamal::elgamal_encrypt(420, 3609, 1234, 3677));
    println!("{}", elgamal::baby_step_giant_step(2, 3, 29));
    */

    //RSA TESTS
    //println!("p, q, n: {:?}", rsa::generate_pqn(1, 10000));
    //println!("e: {:?}", rsa::find_encryption_component(14455043));
    //println!("d = {}", rsa::find_inverse(6701672, 14455043));
    //println!("{}", rsa::encrypt(3981, 3, 12091));
    // ^ result is 
    //println!("{}", rsa::decrypt(12039, 7915, 12091));

    let (p, q, n, phi_n) = rsa::generate_pqn(1, 1000);
    let e = rsa::find_encryption_component(phi_n);
    let d = rsa::find_inverse(e, phi_n);
    let encrypted_message = rsa::encrypt(101, e, n);
    println!("{}", encrypted_message);
    let decrypted_message = rsa::decrypt(encrypted_message, n, d);
    println!("{}", decrypted_message);

}
