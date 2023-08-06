from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.sessioncipher import AESCipher
import hmac, hashlib
def getDerivedKeys(bdata):
    hkdf = HKDFv3()
    derivedSecrets = hkdf.deriveSecrets(bdata, "WhatsApp Image Keys", 112)
    assert len(derivedSecrets) == 112, "Invalid length of derived secret: %s" % len(derivedSecrets)
    iv = derivedSecrets[:16]
    cipherKey = derivedSecrets[16:48]
    macKey = derivedSecrets[48:80]
    refKey = derivedSecrets[80:]
    return DerivedKeys(cipherKey, macKey, iv, refKey)

def encryptImage(imagePath, derivedKeys):
    cipher = AESCipher(derivedKeys.cipherKey, derivedKeys.iv)
    mac = hmac.new(derivedKeys.macKey, derivedKeys.iv, hashlib.sha256)

    with open(imagePath, 'rb') as imageFile:
        data = imageFile.read()
        ciphertext = cipher.encrypt(data)
        return ciphertext + mac.digest()[:10]

def decryptImage(imagePath, derivedKeys):
    cipher = AESCipher(derivedKeys.cipherKey, derivedKeys.iv)
    mac = hmac.new(derivedKeys.macKey, derivedKeys.iv, hashlib.sha256)

    with open(imagePath, 'rb') as imageFile:
        data = imageFile.read()
        data = data[:-10]
        plaintext = cipher.decrypt(data)
        return plaintext



class DerivedKeys(object):
    def __init__(self, cipherKey, macKey, iv, refKey):
        self.cipherKey = cipherKey
        self.macKey = macKey
        self.iv = iv
        self.refKey = refKey
