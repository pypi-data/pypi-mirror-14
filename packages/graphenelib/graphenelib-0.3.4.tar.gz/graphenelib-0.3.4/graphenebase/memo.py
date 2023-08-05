import sys
import hashlib
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from .account import PrivateKey, PublicKey

" This class and the methods require python3 "
assert sys.version_info[0] == 3, "graphenelib requires python3"


def get_shared_secret(priv, pub) :
    """ Derive the share secret between ``priv`` and ``pub``

        :param `Base58` priv: Private Key
        :param `Base58` pub: Public Key
        :return: Shared secret
        :rtype: hex

        The shared secret is generated such that::

            Pub(Alice) * Priv(Bob) = Pub(Bob) * Priv(Alice)

    """
    pub_point  = pub.point()
    priv_point = int(repr(priv), 16)
    res        = pub_point * priv_point
    res_hex    = '%032x' % res.x()
    # Zero padding
    res_hex = '0' * (64 - len(res_hex)) + res_hex
    return res_hex


def init_aes(shared_secret, nonce) :
    """ Initialize AES instance

        :param hex shared_secret: Shared Secret to use as encryption key
        :param int nonce: Random nonce
        :return: AES instance
        :rtype: AES

    """
    " Shared Secret "
    ss     = hashlib.sha512(unhexlify(shared_secret)).digest()
    " Seed "
    seed = bytes(nonce, 'ascii') + hexlify(ss)
    seed_digest = hexlify(hashlib.sha512(seed).digest()).decode('ascii')
    " AES "
    key = unhexlify(seed_digest[0:64])
    iv  = unhexlify(seed_digest[64:96])
    return AES.new(key, AES.MODE_CBC, iv)


def encode_memo(priv, pub, nonce, message) :
    """ Encode a message with a shared secret between Alice and Bob

        :param PrivateKey priv: Private Key (of Alice)
        :param PublicKey pub: Public Key (of Bob)
        :param int nonce: Random nonce
        :param str message: Memo message
        :return: Encrypted message
        :rtype: hex

    """
    shared_secret = get_shared_secret(priv, pub)
    aes           = init_aes(shared_secret, nonce)
    " Checksum "
    raw      = bytes(message, 'utf8')
    checksum = hashlib.sha256(raw).digest()
    raw      = (checksum[0:4] + raw)
    " Padding "
    BS    = 16
    " FIXME: this adds 16 bytes even if not required "
    if len(raw) % BS:
        import struct
        numBytes = (BS - len(raw) % BS)
        pad   = lambda s : s + numBytes * struct.pack('B', numBytes)
        raw   = (pad(raw))
    " Encryption "
    return hexlify(aes.encrypt(raw)).decode('ascii')


def decode_memo(priv, pub, nonce, message) :
    """ Decode a message with a shared secret between Alice and Bob

        :param PrivateKey priv: Private Key (of Bob)
        :param PublicKey pub: Public Key (of Alice)
        :param int nonce: Nonce used for Encryption
        :param bytes message: Encrypted Memo message
        :return: Decrypted message
        :rtype: str
        :raise ValueError: if message cannot be decoded as valid UTF-8
               string

    """
    shared_secret = get_shared_secret(priv, pub)
    aes           = init_aes(shared_secret, nonce)
    " Encryption "
    raw        = bytes(message, 'ascii')
    cleartext  = aes.decrypt(unhexlify(raw))
    " TODO, verify checksum "
    message = cleartext[4:]
    try :
        return message.decode('utf8').strip()
    except :
        raise ValueError(message)

if __name__ == '__main__':
    memo = {"from": "GPH6Co3ctgs6BSsGkti3iVcArMKywbwhnzKDAgmkb6J3Cad7ykDYX",
            "to": "GPH7gU4pHJ9rTUfVA6q6dEgCxgMGVLmq1YM3HRAKpj1VnTzJhrAn2",
            "nonce": "9729217759611568577",
            "message": "aac432f92a8bf52828ac1fda8a3bf6e3"}
    priv = PrivateKey("WIF-KEY")
    pub = PublicKey("OTHERS-PUBKEY", prefix="GPH")
    dec = decode_memo(priv, pub, memo["nonce"], memo["message"])
    print(dec)
