import tempfile
import os
from yowsup.layers.axolotl import mediacipher
from yowsup.layers import YowLayerInterface
class YowAxolotlLayerInterface(YowLayerInterface):
    def trustIdentity(self, identity):
        self.layer.trustIdentity(identity)

    def encryptMedia(self, mediaBuilder):
        fd, encpath = tempfile.mkstemp()
        mediaKey = os.urandom(112)
        keys = mediacipher.getDerivedKeys(mediaKey)
        out = mediacipher.encrypt(mediaBuilder.filepath, keys)
        with open(encpath, 'w') as outF:
            outF.write(out)

        mediaBuilder.setEncryptionData(mediaKey, encpath)
