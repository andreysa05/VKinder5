from peewee import *

db = SqliteDatabase('database.db')


class User(Model):
    user_id = IntegerField()
    offset = IntegerField(default=0)
    couples = TextField()

    class Meta:
        database = db
