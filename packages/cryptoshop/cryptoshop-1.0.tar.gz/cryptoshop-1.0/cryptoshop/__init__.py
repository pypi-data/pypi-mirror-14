#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Cryptoshop version 1.0
    Encrypt and decrypt file in CTR mode with AES, Serpent or Twofish as secure as possible.
    It use only strong algorithms, like Argon2 password derivation, or HMAC(Keccak-1600) for
    authentication.
"""


from cryptoshop.cryptoshop import encryptfile
from cryptoshop.cryptoshop import decryptfile
from cryptoshop.cryptoshop import get_version
