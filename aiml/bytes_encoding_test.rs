use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    println!("args1: {}", args[1]);
    println!("args1 bytes: {:?}", args[1].as_bytes());
    println!("args1 len: {}", args[1].len());

    let mut ctr = 0;
    for character in args[1].chars() {
        let mut b = [0; 4];
        let encoded = character.encode_utf8(&mut b);
        let bytes = encoded.as_bytes();
        let hex: Vec<String> = bytes.iter().map(|b| format!("{:02X}", b)).collect();
    
        ctr = ctr + 1;

        println!("character: {}\tas u32: {}\tencoded: {}\tencoded as bytes: {:?} \tUTF-8 bytes hex: {}", 
            character, 
            character as u32, 
            encoded, 
            encoded.as_bytes(),
            hex.join(" "));
    }
    println!("ctr: {}", ctr);
}
