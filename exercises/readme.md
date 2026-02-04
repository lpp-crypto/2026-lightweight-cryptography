# Exercises



## Lightweight Cryptography

PRESENT[^1] is a lightweight block cipher that was published in 2007. It is optimized for a hardware implementation, but what does it mean in practice?

[^1]: *PRESENT: An Ultra-Lightweight Block Cipher*. Andrey Bogdanov, Lars R. Knudsen, Gregor Leander, Christof Paar, Axel Poschmann, Matthew J. B. Robshaw, Yannick Seurin, C. Vikkelsoe. CHES 2007. https://doi.org/10.1007/978-3-540-74735-2_31. Available on the [https://crypto.orange-labs.fr/papers/ches2007-450.pdf](orange-labs website).



### Hardware-like implementations

**(Q1)** Write a C (or C++) implementation of PRESENT that takes as input an array (or a vector) of 64 booleans as the plaintext, and which evaluates the S-box using its lookup table. Test it against the test vectors provided by its authors.

**(Q2)** Replace the table look-up by the evaluation of a circuit, taking inspiration from the following:

```C
  uint8_t present_sbox(uint8_t * x0, uint8_t * x1, uint8_t * x2, uint8_t * x3)
  {
      uint8_t T1=0, T2=0, T3=0, T4=0, T5=0;
      T1 = (*x2) ^ (*x1) ;
      T2 = (*x1) & T1 ;
      T3 = (*x0) ^ T2 ;
      T5 = (*x3) ^ T3 ;
      T2 = T1 & T3 ;
      T1 = T1 ^ T5 ;
      T2 = T2 ^ (*x1) ;
      T4 = (*x3) | T2 ;
      (*x2) = T1 ^ T4 ;
      (*x3) = ~(*x3) ; 
      T2 = T2 ^ (*x3) ;
      (*x0) = (*x2) ^ T2 ;
      T2 = T2 | T1 ;
      (*x1) = T3 ^ T2 ;
      (*x3) = T5 ;
  }
```

### Software Implementation 


**(Q3)** Write a software implementation of PRESENT and try to make it as fast as possible. Hint: precompute the composition of each S-box with the linear layer.

**(Q4)** Looking back at your implementation in **(Q2)**, What would happen if you simply replaced the type corresponding to boolean variable with, say, `uint_64t`? The corresponding implementation technique is called *bit-slicing*. 

**(Q5)** Compare the throughput (average time taken to process one byte of data) of your bit-sliced implementation with your answer to **(Q4)**.


### Conclusion


**(Q5)** Why is PRESENT good in hardware? Is it good on "regular" computers? What about micro-controllers?



## Standardization

The folder [PIPEAU-cipher](./PIPEAU-cipher/) contains the specification of a new family of 128-bit block ciphers that Borduria is pushing to have standardized. The specification is a simple pdf file called [spec.pdf](./PIPEAU-cipher/spec.pdf), and its authors have provided a reference implementation in Python in the file [reference.py](./PIPEAU-cipher/reference.py). This proves their good faith, right?

**(Q6)** Should this algorithm be standardized? Motivate your answer, keeping in mind that the standardizing body insists on being provided with a technical argument. 
