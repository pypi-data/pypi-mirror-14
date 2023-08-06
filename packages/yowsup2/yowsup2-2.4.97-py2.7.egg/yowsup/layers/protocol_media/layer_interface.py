from yowsup.layers import YowLayerInterface
from yowsup.layers.axolotl.layer import YowAxolotlLayer
from .protocolentities.iq_requestupload import RequestUploadIqProtocolEntity
class YowMediaProtocolLayerInterface(YowLayerInterface):
    def sendImage(self, jid, path, success = None, error = None, progress = None, encrypt=False):
        axolotlLayerInterface = self._layer.getLayerInterface(YowAxolotlLayer)
        if axolotlLayerInterface is None:
            encrypt = False

        #path = encryptImage()
        successFn = lambda resultNode, requestUploadEntity: self.__onRequestUploadSuccess(resultNode, requestUploadEntity, jid, path, success, error, progress, encrypt)
        errorFn = lambda errorNode, requestUploadEntity: self.__onRequestUploadError(errorNode, requestUploadEntity, jid, path, error)
        return self.sendMedia(jid, path, successFn ,errorFn, progress)

    def sendUploadableMedia(self, jid, path, mediaType, success = None, error = None, progress = None):
        iq = RequestUploadIqProtocolEntity(mediaType, filePath = path)
        self._layer._sendIq(iq, success, error, progress)

    def __onRequestUploadSuccess(self, resultNode, requestUploadEntity, jid, path, success = None, error = None, progress = None, encrypt = False):
        pass

    def __onRequestUploadError(self, errorNode, requestUploadEntity, jid, path, error = None):
        if error:
            error(errorNode.code, errorNode.text, errorNode.backoff)
