
#!/usr/bin/python
#
# implementation of key generation  operations
#
# This file is derived from `private_keys.py` in the Chia BLS signatures Python implementation,
#     https://github.com/Chia-Network/bls-signatures/
# which is (C) 2020 Chia Network Inc. and licensed under the Apache 2.0 license.
# See copyright notice at the end of this file.


from __future__ import annotations
from ec import default_ec, G1Generator
from hkdf import extract_expand


class PrivateKey:
    """
    Private keys are just random integers between 1 and the group order.
    """

    PRIVATE_KEY_SIZE = 32

    def __init__(self, value):
        assert value < default_ec.n
        self.value = value

    @staticmethod
    def from_bytes(buffer):
        return PrivateKey(int.from_bytes(buffer, "big") % default_ec.n)

    @staticmethod
    def from_seed(seed):
        L = 48
        # `ceil((3 * ceil(log2(r))) / 16)`, where `r` is the order of the BLS 12-381 curve
        okm = extract_expand(
            L, seed + bytes([0]), b"BLS-SIG-KEYGEN-SALT-", bytes([0, L])
        )
        return PrivateKey(int.from_bytes(okm, "big") % default_ec.n)

    @staticmethod
    def from_int(n: int):
        return PrivateKey(n % default_ec.n)

    def get_g1(self):
        return self.value * G1Generator()

    def sign(self, m):
        pass

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value

    def __bytes__(self):
        return self.value.to_bytes(self.PRIVATE_KEY_SIZE, "big")

    def size(self):
        return self.PRIVATE_KEY_SIZE

    def __str__(self):
        return "PrivateKey(" + hex(self.value) + ")"

    def __repr__(self):
        return "PrivateKey(" + hex(self.value) + ")"

    @staticmethod
    def aggregate(private_keys):
        """
        Aggregates private keys together
        """
        return PrivateKey(sum(pk.value for pk in private_keys) % default_ec.n)


"""
Copyright 2020 Chia Network Inc
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""