# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Union

from cryptography import x509
from cryptography.hazmat.primitives import hashes

__author__ = 'lundberg'

from cryptography.hazmat.primitives.asymmetric.ec import ECDSA, EllipticCurveSignatureAlgorithm

from cryptography.hazmat.primitives.hashes import SHA256, HashAlgorithm

COSE_ALGS = {
    '-65535': 'RS1',
    '-260': 'WalnutDSA',
    '-259': 'RS512',
    '-258': 'RS384',
    '-257': 'RS256',
    '-47': 'ES256K',
    '-46': 'HSS-LMS',
    '-45': 'SHAKE256',
    '-44': 'SHA-512',
    '-43': 'SHA-384',
    '-42': 'RSAES-OAEP w/ SHA-512',
    '-41': 'RSAES-OAEP w/ SHA-256',
    '-40': 'RSAES-OAEP w/ RFC 8017 default parameters',
    '-39': 'PS512',
    '-38': 'PS384',
    '-37': 'PS256',
    '-36': 'ES512',
    '-35': 'ES384',
    '-34': 'ECDH-SS + A256KW',
    '-33': 'ECDH-SS + A192KW',
    '-32': 'ECDH-SS + A128KW',
    '-31': 'ECDH-ES + A256KW',
    '-30': 'ECDH-ES + A192KW',
    '-29': 'ECDH-ES + A128KW',
    '-28': 'ECDH-SS + HKDF-512',
    '-27': 'ECDH-SS + HKDF-256',
    '-26': 'ECDH-ES + HKDF-512',
    '-25': 'ECDH-ES + HKDF-256',
    '-18': 'SHAKE128',
    '-17': 'SHA-512/256',
    '-16': 'SHA-256',
    '-15': 'SHA-256/64',
    '-14': 'SHA-1',
    '-13': 'direct+HKDF-AES-256',
    '-12': 'direct+HKDF-AES-128',
    '-11': 'direct+HKDF-SHA-512',
    '-10': 'direct+HKDF-SHA-256',
    '-8': 'EdDSA',
    '-7': 'ES256',
    '-6': 'direct',
    '-5': 'A256KW',
    '-4': 'A192KW',
    '-3': 'A128KW',
    '0': 'Reserved',
    '1': 'A128GCM',
    '2': 'A192GCM',
    '3': 'A256GCM',
    '4': 'HMAC 256/64',
    '5': 'HMAC 256/256',
    '6': 'HMAC 384/384',
    '7': 'HMAC 512/512',
    '10': 'AES-CCM-16-64-128',
    '11': 'AES-CCM-16-64-256',
    '12': 'AES-CCM-64-64-128',
    '13': 'AES-CCM-64-64-256',
    '14': 'AES-MAC 128/64',
    '15': 'AES-MAC 256/64',
    '24': 'ChaCha20/Poly1305',
    '25': 'AES-MAC 128/128',
    '26': 'AES-MAC 256/128',
    '30': 'AES-CCM-16-128-128',
    '31': 'AES-CCM-16-128-256',
    '32': 'AES-CCM-64-128-128',
    '33': 'AES-CCM-64-128-256',
    '34': 'IV-GENERATION',
}


@dataclass
class CoseAlg:
    hash_alg: HashAlgorithm
    sig_alg: EllipticCurveSignatureAlgorithm

    def hash(self, data: bytes):

def get_cose_alg(alg: int) -> CoseAlg:
    alg_name = COSE_ALGS.get(str(alg))
    if alg_name == 'ES256':
        return CoseAlg(hash_alg=SHA256(), sig_alg=ECDSA(algorithm=SHA256()))
    raise NotImplementedError(f'{alg_name} not implemented')


def load_raw_cert(cert: Union[bytes, str]) -> x509.Certificate:
    if isinstance(cert, bytes):
        cert = cert.decode()
    raw_cert = f'-----BEGIN CERTIFICATE-----\n{cert}\n-----END CERTIFICATE-----'
    return x509.load_pem_x509_certificate(bytes(raw_cert, encoding='utf-8'))
