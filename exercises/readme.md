# Exercises



## Lightweight Cryptography

Rectangle[^1] is a lightweight block cipher that appeared on eprint in 2014. It allows different implementations techniques, which you will need to see for yourself! We will compare it with Present[^2], an older but very influencial lightweight block cipher.


[^1]: *RECTANGLE: a bit-slice lightweight block cipher suitable for multiple platforms*. Wentao Zhang, Zhenzhen Bao, Dongdai Lin, Vincent Rijmen, Bohan Yang, Ingrid Verbauwhede. Sci. China Inf. Sci. 2015.  https://doi.org/10.1007/s11432-015-5459-7. Available on eprint ([eprint/2014/084](http://eprint.iacr.org/2014/084)).

[^2]: *PRESENT: An Ultra-Lightweight Block Cipher*. Andrey Bogdanov, Lars R. Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, Matthew J. B. Robshaw, Yannick Seurin, C. Vikkelsoe. CHES 2007. https://doi.org/10.1007/978-3-540-74735-2_31. Available on the [https://crypto.orange-labs.fr/papers/ches2007-450.pdf](orange-labs website).



### Lookup-based implementations

**(Q1)** Write an implementation of PRESENT that takes as input an array of 64 booleans as the plaintext, and which evaluates the S-box using its lookup table. Test it against the test vectors provided by its authors.

**(Q2)** Same question for RECTANGLE.



### Bit-sliced implementation

**(Q3)** Write a bit-sliced implementation of RECTANGLE, and test it against the test vectors provided by its authors.

**(Q4)** Would a bit-sliced implementation of PRESENT be easy to write? If yes, go ahead; if not, explain why.


## Standardization

The folder [PIPO-cipher](./PIPO-cipher/) contains the specification of a new family of 128-bit block ciphers that Borduria is pushing to have standardized. The specification is a simple pdf file called [spec.pdf](./PIPO-cipher/spec.pdf), and its authors have provided a reference implementation in Python in the file [reference.py](./PIPO-cipher/reference.py). This proves their good faith, right?

**(Q5)** Should this algorithm be standardized? Motivate your answer.
