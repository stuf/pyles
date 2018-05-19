from peewee import *
from ._db import db

class BaseModel(Model):
    class Meta:
        database = db

class File(BaseModel):
    id = IntegerField(primary_key=True)
    file_path = CharField()
    hash = CharField()
    attributes = CharField()

class FileStat(BaseModel):
    accessed = TimestampField(column_name='accessed_time')
    created = TimestampField(column_name='created_time')
    modified = TimestampField(column_name='modified_time')
    permissions = CharField()
    size = IntegerField(default=0)
