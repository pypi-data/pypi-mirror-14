from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import AvailablePresenceProtocolEntity, UnavailablePresenceProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.layers.protocol_contacts.protocolentities import GetSyncIqProtocolEntity
from yowsup_ext.layers.store import YowStorageLayer


import humanthread
import logging

logger = logging.getLogger(__name__)

class YowHumanLayer(YowInterfaceLayer):
    def __init__(self):
        super(YowHumanLayer, self).__init__()
        self.available = False
        self.humanthread = humanthread.HumanThread(self)
        self.humanthread.start()

        self.queuedMessages = {}
        '''
            configs:
                typing speed
                presence
            role:
                place above storage layer
                on send message:
                    if not available
                        send presence available
                    if not a contact:
                        sync along all current contacts data
                    send read notification for all unread messages in this conversation
                    intercept
                    add to queue
                    spawn a thread
                    send typing, paused sequences depending on message length
                    send
                    if queue is empty, send presence unavailable


                on receive message
                    send delivery receipt
                    receive
        '''

    def getStorageLayerInterface(self):
        return self.getStack().getLayerInterface(YowStorageLayer)

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        '''
            When we get a message, immediately send delivered receipt
            and then forward the message to upper layers
        '''
        args = (messageProtocolEntity.getId(),messageProtocolEntity.getFrom(), False)
        if messageProtocolEntity.isGroupMessage():
            args += (messageProtocolEntity.getParticipant(),)
        receipt = OutgoingReceiptProtocolEntity(*args)
        self.toLower(receipt)
        self.toUpper(messageProtocolEntity)


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())
        self.toUpper(entity)


    def send(self, protocolEntity):
        if isinstance(protocolEntity, MessageProtocolEntity):
            self.sendMessage(protocolEntity)
        elif protocolEntity.__class__ == UnavailablePresenceProtocolEntity:
            self.available = False
            self.toLower(protocolEntity)
        else:
            self.toLower(protocolEntity)

    def addNumberToAddressBook(self, numberOrJid):
        contact = self.getStorageLayerInterface().addContact(numberOrJid)
        logger.debug("Added %s to address book, going to sync contacts now" % contact["number"])
        contacts =  self.getStorageLayerInterface().getContacts()
        numbers = [contact["number"] for contact in contacts]
        sync = GetSyncIqProtocolEntity(numbers)

        self._sendIq(sync, self.onSyncResult, self.onSyncError)
        logger.debug("Sent contacts sync request, waiting for response")

    def onSyncResult(self, resultSyncIqProtocolEntity, originalIqEntity):
        inNumbers = resultSyncIqProtocolEntity.inNumbers
        logger.debug("Contacts sync success, in Numbers:\n%s" % ",".join(inNumbers.keys()))
        for jid in self.queuedMessages.keys():
            number = jid.split('@')[0]
            if number in inNumbers.keys():
                queuedMessages = self.queuedMessages[jid]
                logger.debug("We have %s queued messages for the synced '%s', resending" % (len(queuedMessages), number))
                self.queuedMessages[jid] = []
                for message in queuedMessages:
                    self.sendMessage(message)

    def onSyncError(self, errorIqProtocolEntity, originalIqEntity):
        logger.error("Contacts sync errored")

    def sendReceipts(self, messageList, read = False):
        receipts = {}
        for m in messageList:
            conversation = m["conversation"]
            if conversation["type"] == "contact":
                jid = conversation["contact"]["jid"]
            elif conversation["type"] == "group":
                jid = conversation["group"]["jid"]
            else:
                continue

            if jid not in receipts:
                receipts[jid] = []
            receipts[jid].append(m["id"])

        for jid, messageIds in receipts.items():
            receipt = OutgoingReceiptProtocolEntity(messageIds, jid, read=read)

            self.toLower(receipt)

    def queueMessage(self, messageProtocolEntity):
        jid = messageProtocolEntity.getTo()
        if not jid in self.queuedMessages:
            self.queuedMessages[jid] = []

        self.queuedMessages[jid].append(messageProtocolEntity)

        logger.debug("Queued 1 message to %s" % messageProtocolEntity.getTo(False))

    def sendMessage(self, messageProtocolEntity):
        logger.debug("Try sending message to %s" % messageProtocolEntity.getTo(False))


        sinterface = self.getStorageLayerInterface()
        if not messageProtocolEntity.isGroupMessage() and not sinterface.isContact(messageProtocolEntity.getTo()):
            logger.debug("We don't have %s in our addressbook, will add and sync first." % messageProtocolEntity.getTo(False))
            self.queueMessage(messageProtocolEntity)
            self.addNumberToAddressBook("+%s" % messageProtocolEntity.getTo(False))
            return

        if not self.available:
            logger.debug("Our presence is not available, going to send available first")
            self.toLower(AvailablePresenceProtocolEntity())
            self.available = True
        unreadMessages = self.getStorageLayerInterface().getUnreadReceivedMessages(messageProtocolEntity.getTo())
        if len(unreadMessages):
            self.sendReceipts(unreadMessages, read = True)

        self.humanthread.enqueue(messageProtocolEntity)
