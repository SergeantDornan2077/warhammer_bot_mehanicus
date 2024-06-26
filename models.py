from peewee import *

db = SqliteDatabase('data.db')


class User(Model):
    class Meta:
        database = db
        db_table = 'Users'

    vk_id = IntegerField()
    warns = IntegerField()
    rang = TextField()
    chat_id = IntegerField()


class Rangs(Model):
    class Meta:
        database = db
        db_table = "Rangs"
    rang_id = IntegerField()
    rang = TextField()
    chat_id = IntegerField()


class BlackList(Model):
    class Meta:
        database = db
        db_table = "BlackList"
    vk_id = IntegerField()
    chat_id = IntegerField()


class Mut(Model):
    class Meta:
        database = db
        db_table = "Mut"
    vk_id = IntegerField()
    chat_id = IntegerField()


db.create_tables([User, Mut, BlackList, Rangs])
