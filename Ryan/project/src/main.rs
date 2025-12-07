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
    // Ryan decrypts with the ciphertext, g^nonce mod p, Ryan's private key, and p
    println!("Message decrypted: {:?}", elgamal_decrypt(3940, 743, 120, 5393));
    println!("public val: {:?}", elgamal_gen_public_key(3677, 3, 120));
*/

    // ========== EL GAMAL ==========
    /* 
    // Leonidas
    // prime = 8837, generator = 2
    // public key = 6412
    // my random r = 182
    // generate public key
    let pub_key = elgamal::elgamal_gen_public_key(8837, 2, 182);
    //println!("{}", pub_key);
    // my public key generated = 4471
    let leonidas_message = 543 as i128;
    let leonidas_encrypted_message = elgamal::elgamal_encrypt(leonidas_message, 6412, 182, 8837);
    println!("Encrypted message: {}\nRyan's public key: {}", leonidas_encrypted_message, pub_key);
*/


    //println!("p = 3677");
    //println!("primitive root = {}", elgamal::find_primitive_root(3677));
    //println!("my public val: 683");
    //println!("decrypted: {}", elgamal::elgamal_decrypt(1942, 2341, 1234, 3677));
    //private key is 1234
    //println!("encrypted: {}", elgamal::elgamal_encrypt(420, 3609, 1234, 3677));
    //println!("{}", elgamal::elgamal_intercept(3107, 2, 683, 3609, 3677));
    

    // ==========   RSA    ==========
    //println!("p, q, n: {:?}", rsa::generate_pqn(1, 10000));
    //println!("e: {:?}", rsa::find_encryption_component(14455043));
    //println!("d = {}", rsa::find_inverse(6701672, 14455043));
    //println!("{}", rsa::encrypt(3981, 3, 12091));
    // ^ result is 
    //println!("{}", rsa::decrypt(12039, 7915, 12091));
  
    let (p, q, n, phi_n) = rsa::generate_pqn(1000, 10000);
    //println!("p: {}, q: {}, n: {}, phi_n: {}", p, q, n, phi_n);
    let e = rsa::find_encryption_component(phi_n);
    //println!("encryption component: {}", e);
    let d = rsa::find_inverse(e, phi_n);
    //println!("d: {}", d);
    let message = 67420;
    //println!("original message: {}", message);
    let encrypted_message = rsa::encrypt(message, e, n);
    //println!("encrypted message: {}", encrypted_message);
    let decrypted_message = rsa::decrypt(encrypted_message, n, d);
    //println!("decrypted message: {}", decrypted_message);

    //let rsa_alexan_n = 48425303 as i128;
    //let rsa_alexan_e = 65537 as i128;
    //let alexan_message = 890 as i128;
    //let rsa_alexan_msg_encrypted = rsa::encrypt(alexan_message, rsa_alexan_e, rsa_alexan_n);
    //println!("{}", rsa_alexan_msg_encrypted);
    // encrypted message = 18575837
    // alexan sends encrypted message: 19152381
    //let rsa_alexan_msg_decrypted = rsa::decrypt(13699320, 24673183, 1107525);
    //println!("{}", rsa_alexan_msg_decrypted);
    //println!("{}", rsa::rsa_intercept(3719979, 18228547, 16143173));

}
