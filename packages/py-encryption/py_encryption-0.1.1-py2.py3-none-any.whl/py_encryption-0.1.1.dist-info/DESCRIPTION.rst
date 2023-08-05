py-encryption
=============

Simple Encryption in Python (ported from https://github.com/defuse/php-encryption).

This is a class for doing symmetric encryption in Python.

Implementation
--------------

Messages are encrypted with AES-128 in CBC mode and are authenticated with
HMAC-SHA256 (Encrypt-then-Mac). PKCS7 padding is used to pad the message to
a multiple of the block size. HKDF is used to split the user-provided key into
two keys: one for encryption, and the other for authentication. It is
implemented using the `Crypto` and `hmac` modules.

Authors
---------

This port was based on the library authored by Taylor Hornby and Scott Arciszewski.


