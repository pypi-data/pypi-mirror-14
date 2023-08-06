from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
class YowInMemoryStorageLayer(YowInterfaceLayer):

    def __init__(self):
        super(YowInMemoryStorageLayer, self).__init__()
        self.outgoingStore = {}

    def send(self, protocolEntity):
        if isinstance(protocolEntity, MessageProtocolEntity):
            self.storeOutgoingMessage()
            self.toLower(protocolEntity)

    def storeOutgoingMessage(self):
        pass