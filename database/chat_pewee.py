from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, DateField
from datetime import datetime, timezone

db = SqliteDatabase("chat_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField()
    user_id = IntegerField()
    username = CharField()
    date = DateField(default=datetime.now(timezone.utc))
    msg = CharField()

    def __str__(self):
        return "{date}: {msg}".format(date=self.date, msg=self.msg)


def create_models():
    db.create_tables([User], safe=True)


# if __name__ == '__main__':
#     create_models()


