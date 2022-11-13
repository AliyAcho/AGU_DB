from peewee import * 
db = SqliteDatabase('test.db')


class orders(Model):
    name = CharField(max_length=255, primary_key=True)
    avg_count = IntegerField(default=0)
    take_count = IntegerField(default=0)
    
    class Meta:
        database = db

class student(Model):
    first_name = CharField(max_length=255, primary_key=True)
    last_name = CharField(max_length=255)
    
    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([orders, student, ])
    return True


res = create_tables()
