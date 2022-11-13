from peewee import *
from playhouse.reflection import generate_models, print_model, print_table_sql


db = SqliteDatabase('test.db')
models = generate_models(db)
globals().update(models)
tables = db.get_tables()
for table_name in tables:
    columns = db.get_columns(table_name)
    print(table_name)
    for column in columns:
        print(f"{column.name}")
        len_student = eval(f"len({table_name}.select())")
        for i in range(len_student):
            name = eval(f"{table_name}.select()[{i}].{column.name}")
            print(name)
    print("--------------")

def get_table_name(table_name):
    names = []
    columns = db.get_columns(table_name)
    for column in columns:
        names.append(column.name)
    return names