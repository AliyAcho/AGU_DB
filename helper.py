from peewee import *
from playhouse.reflection import generate_models


class DatabaseHelper:
    def __init__(self, file_name):
        self.db = SqliteDatabase(file_name)
        models = generate_models(self.db)
        globals().update(models)
        self.tables = self.db.get_tables()

    def get_column_name(self, table_name):
        names = []
        columns = self.db.get_columns(table_name)
        for column in columns:
            names.append(column.name)
        return names

    def get_columns_data(self, table_name):
        data = []
        columns = self.db.get_columns(table_name)
        len_student = eval(f"len({table_name}.select())")
        for i in range(len_student):
            data_inner = []
            for column in columns:
                name = eval(f"{table_name}.select()[{i}].{column.name}")
                data_inner.append(name)
            data.append(data_inner)
        return data
