Cryptoshop
===============
A Python 3 module to encrypt and decrypt file in CTR mode with AES, Serpent or Twofish as secure as possible.

***(C)2016 @ CORRAIRE Fabrice***
antidote1911@gmail.com

Cryptoshop is the crypto module of [Cryptoshop-GUI](https://github.com/Antidote1911/Cryptoshop-GUI) (a Qt5 application
for use this module and GnuPG graphically.

General Specifications :
-----------------
To install: python setup.py install

Cryptoshop encrypt files with one of this three algorithms in [CTR mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation):
- [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [Serpent](https://en.wikipedia.org/wiki/Serpent_%28cipher%29)
- [Twofish](https://en.wikipedia.org/wiki/Twofish)

It use Botan. Crypto and TLS library for C++11.
For more information's on Botan, go here:
- http://botan.randombit.net
- https://github.com/randombit/botan
- https://en.wikipedia.org/wiki/Botan_(programming_library)

It use Argon2 for key derivation/stretching and HMAC-Keccak-1600 for message authentication.
For more information's on Argon2:
- https://en.wikipedia.org/wiki/Argon2
- https://www.cryptolux.org/index.php/Argon2
- https://github.com/P-H-C/phc-winner-argon2

Cryptoshop is optimized for large files.

<b>You can use it like console application:</b>

Linux users: Make a symlink of the module on your bin folder...

    # encrypt the file test with AES-256.
    # If no algo is specified, Serpent (-a srp) is default.
    # Encrypted file test.cryptoshop is write in same folder:

    ./cryptoshop -e test -a aes


    # decrypt the file test.cryptoshop.
    # No need to specify algo. It is automatically detected by decryption routine.

    ./cryptoshop -d test.cryptoshop


<b>You can use it like a module for your Python application:</b>

    from cryptoshop import encryptfile
    from cryptoshop import decryptfile

    result = encryptfile(filename="test", passphrase="mypassphrase", algo="srp")
    print(result["success"])

    result = decryptfile(filename="test.cryptoshop", passphrase="mypassphrase")
    print(result["success"])

Advanced Specifications :
-----------------
####<u>1- Key derivation/stretching :</u>

The user passphrase derivation is performed with the winner of the Password Hashing Competition, [Argon2](https://en.wikipedia.org/wiki/Argon2).
Argon2 use a fixed timing calculation and not iterations, to prevent [Timing attack](https://en.wikipedia.org/wiki/Timing_attack).

####<u>2- Encryption :</u>

You can encrypt with AES-256, Serpent-256, or Twofish-256. If no algorithm is specified, Cryptoshop use Serpent-256.


- A random 512 bits 'master_salt' is generated. It is split in two 256 bits salts. One for Argon2 derivation and one for authentication.
- Argon2 generate a 512 bits master-key with the user passphrase and one of the two 256 bits salt.
- This key is split in two 256 bits keys. One for encrypt the random 256 bits 'internal-key' and one for authenticate the encrypted 'internal-key'.

Encryption is optimized for larges files.

The file is encrypted chunk by chunk with the 'internal-key'. Etch iteration calculate an 'internal-hmac'. All encrypted chunks use a different
random 16 bits nonce (or initialization vector if you want...). It is ABSOLUTELY necessary for CTR mode...
[NEVER USE THE SAME KEY WITH THE SAME NONCE](http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ctr/ctr-spec.pdf).

The final Cryptoshop format is:

    ***************************************************
    -header                                 18 bits   *
    -pass-salt || hmac-salt          256 + 256 bits   *
    -hmac                                  512 bits   *
    ***************************                       *
    nonce || encrypted_internal_key  128 + 256 bits   *
    hmac_internal                          512 bits   *
    internal_salt                    256 + 256 bits   *
    ---------------------------                       *
    nonce1 || cipherchunk1       128 bits + chunkSize *
    ---------------                                   *
    nonce2 || cipherchunk2       128 bits + chunkSize *
    ---------------                                   *
    nonce3 || cipherchunk3       128 bits + chunkSize *
    ---------------                                   *
    nonceN || cipherchunkN       128 bits + chunkSize *
    ---------------                                   *
    ***************************************************

128 bits = 16 bytes

256 bits = 32 bytes

chunksize is fixed to 0,5 Mo (500000 bytes)

####<u>3- Decryption :</u>

- The decryption routine check the header before all other operations.
- The hmac of the 'encrypted-key' is verified.
- If the hmac is correct, the 'encrypted-key' is decrypted.
- The decryption routine decrypt all chunks with this 'decrypted-key'
- The internal-hmac is verified



####<u>4- Authentication :</u>

Authentication is performed by HMAC(Keccak-1600). Keccak-1600 is the Winner Of SHA-3 Competition.

More information here:
- https://en.wikipedia.org/wiki/SHA-3
- http://keccak.noekeon.org/

The two authentication (master and internal) are calculated with the encrypted data. NOT WITH CLEAR DATA.

The decryption routine read the two hmac code in the encrypted file, and compare it with the calculated values.
Cryptoshop use a constant timing algorithm verification to prevent Timing Attack. Not a naive <i>if hamac1 == hmac2</i>

##Requirement
- Python >= 3
- Botan library >=1.11 <---  Install the last version (1.29). Cryptoshop don't work with the 1.10 branch.
The installation include the Python wrapper.

Python modules:
- [tqdm](https://github.com/tqdm/tqdm)  <--- console progress-bar
- [argon2_cffi](https://github.com/hynek/argon2_cffi) <--- Python module/wrapper for Argon2


##License

- Cryptoshop is released under [GPL3](https://github.com/Antidote1911/cryptoshop/blob/master/cryptoshop.license) License.
- Botan is released under the permissive [Simplified BSD](http://botan.randombit.net/license.txt) license.
- argon2_cffi and tqdm are released under The [MIT](https://github.com/hynek/argon2_cffi/blob/master/LICENSE) License

##Why Cryptoshop ?

There is a lot of bad encryption modules for python.
- no authentication.
- else, authentication routine use naive comparison like <i>if m1==m2 mac is good</i>. This approach permit Timing Attack.
- use unsecured algorithm like ECB mode, MD5 or SHA-1 etc...
- bad use of the encryption mode. Reuse nonce for same key in CTR, fixed initialization vector when it must be random etc...
- Passphrase derivation/stretching with iterative hash function. Good for brute-force with GPU ! Hash are NOT make for this usage. Use strong Key Derivation Functions (KDF) algo like Argon2 or PBKDF2.
- Systematically use PyCrypto. This is a good module, but there is no Serpent algo, and some algo like PBKDF2 are very slow because it's a pure Python implementation.
- No optimization for big files.
etc ...

A very good encryption module is [simple-crypt](https://github.com/andrewcooke/simple-crypt) but the usage of PyCrypto eliminate the usage of Serpent, and make PBKDF2 very slow. Finally, it was't designed for encrypt big files.
This is my choice for encrypt string with AES in CTR mode.

##Other resources
Same recommendations of the [Botan author](http://botan.randombit.net/):

<i>"You should have some knowledge of cryptography *before* trying to use
or modify this module. This is an area where it is very easy to make mistakes,
and where things are often subtle and/or counterintuitive.

The module tries to provide things at a high level precisely to
minimize the number of ways things can go wrong, but naive modifications will
almost certainly not result in a secure system.

Especially recommended are:

- *Cryptography Engineering*
  by Niels Ferguson, [Bruce Schneier](https://www.schneier.com/), and Tadayoshi Kohno

- *Security Engineering -- A Guide to Building Dependable Distributed Systems*
  by Ross Anderson
  [available online](https://www.cl.cam.ac.uk/~rja14/book.html)

- *Handbook of Applied Cryptography*
by Alfred J. Menezes, Paul C. Van Oorschot, and Scott A. Vanstone
[available online](http://www.cacr.math.uwaterloo.ca/hac/)

If you're doing something non-trivial or unique, you might want to at
the very least ask for review/input on a mailing list such as the
[metzdowd](http://www.metzdowd.com/mailman/listinfo/cryptography) or
[randombit](http://lists.randombit.net/mailman/listinfo/cryptography)
crypto lists. And (if possible) pay a professional cryptographer or
security company to review your design and code."</i>


http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf

http://www.daemonology.net/blog/2009-06-11-cryptographic-right-answers.html

https://en.wikipedia.org/wiki/Timing_attack
