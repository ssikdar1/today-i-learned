# UTF8 String Craziness

While brainstorming about creating a rust program to implement Byte Pair Encoding, I was reminded just how strange and unintuitive text can be, especially in other languages. I will get to actually implementing BPE at some other date but wanted to document some discoveries.

## Quick Recap

When looking at a line of text. (e.g. `hello world`) while we humans in terms of letters `h`, `e`, ... computers actually think of text in terms of numbers. Specifically Rust's `String` type thinks in terms of numbers in utf-8 encoding that maps to symbols in the [Unicode Standard](https://en.wikipedia.org/wiki/List_of_Unicode_characters).

## English difficulty mode: Easy

So let's take the following rust code and look at how it behaves with  English input.

The program is simply doing the following:
* Take an input argument string. Print the string, bytes, and length of the array of bytes.
* Iterate through each character of the string. For each character:
    * print the character
    * print the character encoded as utf8
    * print that encoded utf8's bytes
    * print the hex value of the utf8
    * print how many times it looped through the characters. ( aka how many characters are in my string )

```{rust}
  1 use std::env;
  2 
  3 fn main() {
  4     let args: Vec<String> = env::args().collect();
  5 
  6     println!("args1: {}", args[1]);
  7     println!("args1 bytes: {:?}", args[1].as_bytes());
  8     println!("args1 len: {}", args[1].len());
  9 
 10     let mut ctr = 0;
 11     for character in args[1].chars() {
 12         let mut b = [0; 4];
 13         let encoded = character.encode_utf8(&mut b);
 14         let bytes = encoded.as_bytes();
 15         let hex: Vec<String> = bytes.iter().map(|b| format!("{:02X}", b)).collect();
 16 
 17         ctr = ctr + 1;
 18 
 19         println!("character: {}\tas u32: {}\tencoded: {}\tencoded as bytes: {:?} \tUTF-8 bytes hex: {}",
 20             character,
 21             character as u32,
 22             encoded,
 23             encoded.as_bytes(),
 24             hex.join(" "));
 25     }
 26     println!("ctr: {}", ctr);
```

lets look at its output of the program with the string `Hello World`:

```
$ ./bpe "hello world"
args1: hello world
args1 bytes: [104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100]
args1 len: 11
character: h	as u32: 104	encoded: h	encoded as bytes: [104] 	UTF-8 bytes hex: 68
character: e	as u32: 101	encoded: e	encoded as bytes: [101] 	UTF-8 bytes hex: 65
character: l	as u32: 108	encoded: l	encoded as bytes: [108] 	UTF-8 bytes hex: 6C
character: l	as u32: 108	encoded: l	encoded as bytes: [108] 	UTF-8 bytes hex: 6C
character: o	as u32: 111	encoded: o	encoded as bytes: [111] 	UTF-8 bytes hex: 6F
character:  	as u32: 32	encoded:  	encoded as bytes: [32] 	UTF-8 bytes hex: 20
character: w	as u32: 119	encoded: w	encoded as bytes: [119] 	UTF-8 bytes hex: 77
character: o	as u32: 111	encoded: o	encoded as bytes: [111] 	UTF-8 bytes hex: 6F
character: r	as u32: 114	encoded: r	encoded as bytes: [114] 	UTF-8 bytes hex: 72
character: l	as u32: 108	encoded: l	encoded as bytes: [108] 	UTF-8 bytes hex: 6C
character: d	as u32: 100	encoded: d	encoded as bytes: [100] 	UTF-8 bytes hex: 64
ctr: 11
```

As we can see the output is pretty boring. There are 11 letters and 11 bytes in the array. Each character correspondes to a byte in the array. 

## Et en Francais?

Let's now try running the program with the official motto of France: `Liberté, égalité, fraternité`

```
$ ./bpe "Liberté, égalité, fraternité"
args1: Liberté, égalité, fraternité
args1 bytes: [76, 105, 98, 101, 114, 116, 195, 169, 44, 32, 195, 169, 103, 97, 108, 105, 116, 195, 169, 44, 32, 102, 114, 97, 116, 101, 114, 110, 105, 116, 195, 169]
args1 len: 32
character: L	as u32: 76	encoded: L	encoded as bytes: [76] 	UTF-8 bytes hex: 4C
character: i	as u32: 105	encoded: i	encoded as bytes: [105] 	UTF-8 bytes hex: 69
character: b	as u32: 98	encoded: b	encoded as bytes: [98] 	UTF-8 bytes hex: 62
character: e	as u32: 101	encoded: e	encoded as bytes: [101] 	UTF-8 bytes hex: 65
character: r	as u32: 114	encoded: r	encoded as bytes: [114] 	UTF-8 bytes hex: 72
character: t	as u32: 116	encoded: t	encoded as bytes: [116] 	UTF-8 bytes hex: 74
character: é	as u32: 233	encoded: é	encoded as bytes: [195, 169] 	UTF-8 bytes hex: C3 A9
character: ,	as u32: 44	encoded: ,	encoded as bytes: [44] 	UTF-8 bytes hex: 2C
character:  	as u32: 32	encoded:  	encoded as bytes: [32] 	UTF-8 bytes hex: 20
character: é	as u32: 233	encoded: é	encoded as bytes: [195, 169] 	UTF-8 bytes hex: C3 A9
character: g	as u32: 103	encoded: g	encoded as bytes: [103] 	UTF-8 bytes hex: 67
character: a	as u32: 97	encoded: a	encoded as bytes: [97] 	UTF-8 bytes hex: 61
character: l	as u32: 108	encoded: l	encoded as bytes: [108] 	UTF-8 bytes hex: 6C
character: i	as u32: 105	encoded: i	encoded as bytes: [105] 	UTF-8 bytes hex: 69
character: t	as u32: 116	encoded: t	encoded as bytes: [116] 	UTF-8 bytes hex: 74
character: é	as u32: 233	encoded: é	encoded as bytes: [195, 169] 	UTF-8 bytes hex: C3 A9
character: ,	as u32: 44	encoded: ,	encoded as bytes: [44] 	UTF-8 bytes hex: 2C
character:  	as u32: 32	encoded:  	encoded as bytes: [32] 	UTF-8 bytes hex: 20
character: f	as u32: 102	encoded: f	encoded as bytes: [102] 	UTF-8 bytes hex: 66
character: r	as u32: 114	encoded: r	encoded as bytes: [114] 	UTF-8 bytes hex: 72
character: a	as u32: 97	encoded: a	encoded as bytes: [97] 	UTF-8 bytes hex: 61
character: t	as u32: 116	encoded: t	encoded as bytes: [116] 	UTF-8 bytes hex: 74
character: e	as u32: 101	encoded: e	encoded as bytes: [101] 	UTF-8 bytes hex: 65
character: r	as u32: 114	encoded: r	encoded as bytes: [114] 	UTF-8 bytes hex: 72
character: n	as u32: 110	encoded: n	encoded as bytes: [110] 	UTF-8 bytes hex: 6E
character: i	as u32: 105	encoded: i	encoded as bytes: [105] 	UTF-8 bytes hex: 69
character: t	as u32: 116	encoded: t	encoded as bytes: [116] 	UTF-8 bytes hex: 74
character: é	as u32: 233	encoded: é	encoded as bytes: [195, 169] 	UTF-8 bytes hex: C3 A9
ctr: 28
```

Things immediately have gotten a little weirder. There are only 28 letters and yet the byte buffer as 32 entries!

With english we got lucky since the code points of all english characters in the Unicode Standard can be fit within one byte. However in French with the `é` we've gotten unlucky. Each `é` is represented by C3 A9 and therfore needsZ two bytes to fit that information.

## Now in Hindi

Now lets try running the program with the string `हैलो वर्ल्ड` which is literally hello world spelt phonetically with the devnagari script.

```
$ ./bpe "हैलो वर्ल्ड"
args1: हैलो वर्ल्ड
args1 bytes: [224, 164, 185, 224, 165, 136, 224, 164, 178, 224, 165, 139, 32, 224, 164, 181, 224, 164, 176, 224, 165, 141, 224, 164, 178, 224, 165, 141, 224, 164, 161]
args1 len: 31
character: ह	as u32: 2361	encoded: ह	encoded as bytes: [224, 164, 185] 	UTF-8 bytes hex: E0 A4 B9
character: ै	as u32: 2376	encoded: ै	encoded as bytes: [224, 165, 136] 	UTF-8 bytes hex: E0 A5 88
character: ल	as u32: 2354	encoded: ल	encoded as bytes: [224, 164, 178] 	UTF-8 bytes hex: E0 A4 B2
character: ो	as u32: 2379	encoded: ो	encoded as bytes: [224, 165, 139] 	UTF-8 bytes hex: E0 A5 8B
character:  	as u32: 32	encoded:  	encoded as bytes: [32] 	UTF-8 bytes hex: 20
character: व	as u32: 2357	encoded: व	encoded as bytes: [224, 164, 181] 	UTF-8 bytes hex: E0 A4 B5
character: र	as u32: 2352	encoded: र	encoded as bytes: [224, 164, 176] 	UTF-8 bytes hex: E0 A4 B0
character: ्	as u32: 2381	encoded: ्	encoded as bytes: [224, 165, 141] 	UTF-8 bytes hex: E0 A5 8D
character: ल	as u32: 2354	encoded: ल	encoded as bytes: [224, 164, 178] 	UTF-8 bytes hex: E0 A4 B2
character: ्	as u32: 2381	encoded: ्	encoded as bytes: [224, 165, 141] 	UTF-8 bytes hex: E0 A5 8D
character: ड	as u32: 2337	encoded: ड	encoded as bytes: [224, 164, 161] 	UTF-8 bytes hex: E0 A4 A1
ctr: 11
```

Here we see an even greater disparity between the number of letters present in the string and the length of the buffer! 
Every single character takes up 3 bytes. 

Reading through documentation for [encode_utf8](https://doc.rust-lang.org/std/primitive.char.html) we see that 4 bytes is the max any character can have.

## Conclusion and Notes
In conclusion Strings can be more intuitive than they appear in first glance! There are many other odd quirks when working in different languages but I'm blanking on them now. A few other issues that come up are:
* CJK / Han Unification
* In many Indian languages have componund letters that are created by combining other letters into one. However there is no code point for those letters. So for example putting the word `नवरात्री` into the script the final letter त्री is actually created with three separate letters:

```
$ ./bpe "नवरात्री"
args1: नवरात्री
args1 bytes: [224, 164, 168, 224, 164, 181, 224, 164, 176, 224, 164, 190, 224, 164, 164, 224, 165, 141, 224, 164, 176, 224, 165, 128]
args1 len: 24
character: न	as u32: 2344	encoded: न	encoded as bytes: [224, 164, 168] 	UTF-8 bytes hex: E0 A4 A8
character: व	as u32: 2357	encoded: व	encoded as bytes: [224, 164, 181] 	UTF-8 bytes hex: E0 A4 B5
character: र	as u32: 2352	encoded: र	encoded as bytes: [224, 164, 176] 	UTF-8 bytes hex: E0 A4 B0
character: ा	as u32: 2366	encoded: ा	encoded as bytes: [224, 164, 190] 	UTF-8 bytes hex: E0 A4 BE
character: त	as u32: 2340	encoded: त	encoded as bytes: [224, 164, 164] 	UTF-8 bytes hex: E0 A4 A4
character: ्	as u32: 2381	encoded: ्	encoded as bytes: [224, 165, 141] 	UTF-8 bytes hex: E0 A5 8D
character: र	as u32: 2352	encoded: र	encoded as bytes: [224, 164, 176] 	UTF-8 bytes hex: E0 A4 B0
character: ी	as u32: 2368	encoded: ी	encoded as bytes: [224, 165, 128] 	UTF-8 bytes hex: E0 A5 80
ctr: 8
```



# Running Questions for myself.

* Does this change how I would implement Byte Pair Encoding in different languages? Or does it remain agnostic to these differences? 



# AI Disclaimer

I feel similar to how there are warning labels on cigarettes, there should be a general warning on how much AI was used in any endeavor. In this case I did use claude to figure out how to encode a character from a `String` to utf8 hex. The encoding it into a buffer of bytes didn't occur to me.