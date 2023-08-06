from yowsup.layers import YowLayer
from yowsup.common.tools import StorageTools
import peewee
import datetime

DB_NAME = StorageTools.constructPath("yow.db")
db = peewee.SqliteDatabase(DB_NAME, threadlocals=True)

class BaseModel(peewee.Model):
    class Meta:
        database = db

class State(BaseModel):
    name = peewee.CharField()

class Message(BaseModel):
    conversation = peewee.ForeignKeyField(Conversation)
    created = peewee.DateTimeField(datetime.datetime.now())
    t_sent = peewee.DateTimeField()
    content = peewee.TextField()
    media = peewee.ForeignKeyField(Media, null=True)

class MessageState(BaseModel):
    message = peewee.ForeignKeyField(Message)
    state = peewee.ForeignKeyField(State)
    contact = peewee.ForeignKeyField(Contact, null=True)

class Conversation(BaseModel):
    contact = peewee.ForeignKeyField(Contact, null=True)
    group = peewee.ForeignKeyField(Group, null = True)
    broadcast = peewee.ForeignKeyField(Broadcast, null=True)
    created = peewee.DateTimeField(datetime.datetime.now())

class Contact(BaseModel):
    number = peewee.CharField(unique=True)
    jid = peewee.CharField()
    last_seen_on = peewee.DateTimeField()
    status = peewee.CharField()
    push_name = peewee.CharField()
    name = peewee.CharField()
    source_id= peewee.CharField(null=True) #id in data source, like in phone addreess book
    picture = peewee.BlobField()

class Group(BaseModel):
    jid = peewee.CharField()
    picture = peewee.BlobField()
    subject = peewee.CharField()
    subject_owner_id = peewee.ForeignKeyField(Contact)
    subject_time = peewee.DateTimeField()
    created = peewee.DateTimeField(default=datetime.datetime.now())

class GroupContact(BaseModel):
    contact = peewee.ForeignKeyField(Contact)
    group = peewee.ForeignKeyField(Group)

class MediaType(BaseModel):
    type = peewee.CharField()

class Media(BaseModel):
    type = peewee.ForeignKeyField(MediaType)
    preview = peewee.CharField()
    remote_url = peewee.CharField()
    local_path = peewee.CharField(null = True)
    data = peewee.BlobField(null = True)
    transfer_status = peewee.IntegerField(default=0)
    size = peewee.IntegerField()

class Status(BaseModel):
    text = peewee.TextField()
    created = peewee.DateTimeField(default=datetime.datetime.now())

class Broadcast(BaseModel):
    wId = peewee.CharField() #Can't remember so far what that was for, but it's in openwa so maybe important
    created = peewee.DateTimeField(default=datetime.datetime.now())

class BroadcastContact(BaseModel):
    contact = peewee.ForeignKeyField(Contact)
    broadcast = peewee.ForeignKeyField(Broadcast)

db.connect()
db.create_tables([
    State,
    Message,
    MessageState,
    Conversation,
    Contact,
    Group,
    GroupContact,
    MediaType,
    Media,
    State,
    Broadcast,
    BroadcastContact
])




class SqliteStorageLayer(YowLayer):
    pass