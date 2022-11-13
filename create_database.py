from peewee import *


db = SqliteDatabase('orders.db')


class Orders(Model):
    name = CharField(max_length=255, primary_key=True)
    avg_count = IntegerField(default=0)
    take_count = IntegerField(default=0)

    class Meta:
        database = db  # модель будет использовать базу данных 'orders.db'


class Student(Model):
    first_name = CharField(max_length=255, primary_key=True)
    last_name = CharField(max_length=255)

    class Meta:
        database = db  # модель будет использовать базу данных 'orders.db'


def create_tables():
    with db:
        db.create_tables([Student, Orders,])

create_tables()

Student.create(first_name="Aliy", last_name="Achmizov")
Student.create(first_name="Dmitry", last_name="Deinega")
Orders.create(name="Banana")
Orders.create(name="Potato")
db.commit()