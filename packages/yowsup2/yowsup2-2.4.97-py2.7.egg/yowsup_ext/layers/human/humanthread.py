import threading
import time
import Queue

from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import UnavailablePresenceProtocolEntity

DEFAULT_OPTS = {
    "speed_typing": 50, #words/minute
    "speed_mediaselect": 7 #seconds
}

class HumanThread(threading.Thread):
    def __init__(self, interfaceLayer, options = None):
        super(HumanThread, self).__init__()
        self.daemon = True
        self.queue = Queue.Queue()
        self.interfaceLayer = interfaceLayer
        self.opts = {}
        self.opts.update(DEFAULT_OPTS)
        if options is not None:
            self.opts.update(options)

        self.wps = self.opts["speed_typing"] / 60.0

    def enqueue(self, messageProtocolEntity):
        self.queue.put(messageProtocolEntity)

    def run(self):
        while True:
            messageProtocolEntity = self.queue.get()
            if messageProtocolEntity.getType() == messageProtocolEntity.MESSAGE_TYPE_TEXT:
                words = messageProtocolEntity.getBody().split(' ')

                composingChatState = OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_TYPING,
                    messageProtocolEntity.getTo()
                )
                pausedChatState = OutgoingChatstateProtocolEntity(
                    OutgoingChatstateProtocolEntity.STATE_PAUSED,
                    messageProtocolEntity.getTo()
                )
                time.sleep(2)
                self.interfaceLayer.toLower(composingChatState)
                for i in range(0, len(words)):
                    time.sleep(self.wps)

                self.interfaceLayer.toLower(pausedChatState)
                time.sleep(0.5)
            else:
                time.sleep(self.opts["speed_mediaselect"])

            self.interfaceLayer.toLower(messageProtocolEntity)

            if self.queue.empty():
                self.interfaceLayer.send(UnavailablePresenceProtocolEntity())
