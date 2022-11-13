"""
Задание:
Написать скрипт который передает любую простейшую базу в google таблицы и наоборот из гугл таблицы обратно в базу
"""
from google_apis import create_service
from helper import DatabaseHelper

# Подключаемся к апи гугл таблиц
CLIENT_FILE = 'client_secret_483810097087-n3o0qhanldmoajlu9trf8k9vt31ubdph.apps.googleusercontent.com.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https:#www.googleapis.com/auth/spreadsheets']
service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
GOOGLE_SHEETS_ID = '1zXR8GR8E-cnZT-j231ZBcJzp5zLIEeSthsfDuHBFr98'

helper = DatabaseHelper("orders.db")


def db_to_exel():
    # Один лист - одна таблица из бд
    for table in helper.tables:
        # Создаем лист
        try:
            service.spreadsheets().batchUpdate(
                spreadsheetId=GOOGLE_SHEETS_ID,
                body={
                    "requests": [{
                        "addSheet": {
                            # Add properties for the new sheet
                            "properties": {
                                "title": table,
                            }
                        },
                    }]
                }
            ).execute()
        except:
            pass
        # Вставляем названия столбцов
        service.spreadsheets().values().update(
            spreadsheetId=GOOGLE_SHEETS_ID,
            range=f"{table}!A1",
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': [helper.get_column_name(table)]
            }
        ).execute()
        # Вставляем данные
        columns_data = helper.get_columns_data(table)
        service.spreadsheets().values().update(
            spreadsheetId=GOOGLE_SHEETS_ID,
            range=f"{table}!A2",
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': [column_data for column_data in columns_data]
            }
        ).execute()


def exel_to_db():
    data = service.spreadsheets().getByDataFilter(spreadsheetId=GOOGLE_SHEETS_ID).execute()
    database_name = data["properties"]["title"]
    with open(f"create_model_{database_name}.py", "w") as f:
        f.write(f"from peewee import * \n"
                f"db = SqliteDatabase('{database_name}.db')\n\n")
        titles_string = ""
        for sheet in data["sheets"]:
            title = sheet["properties"]["title"]
            data_sheet = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_ID, ranges=title, includeGridData=True).execute()
            i = 0
            f.writelines(f"\nclass {title}(Model):\n    ")
            model_fields = []
            for name in data_sheet["sheets"][0]["data"][0]["rowData"][0]["values"]:
                name_field = name["userEnteredValue"]["stringValue"]
                type_field = list(data_sheet["sheets"][0]["data"][0]["rowData"][1]["values"][i]["userEnteredValue"].keys())[0]
                if i == 0:
                    pk = ", primary_key=True"
                else:
                    pk = ""
                if type_field == "numberValue":
                    type_field = f"IntegerField(default=0{pk})"
                else:
                    type_field = f"CharField(max_length=255{pk})"
                f.write(f"{name_field} = {type_field}\n    ")
                i += 1
            titles_string = titles_string + title + ", "
            f.write(f"\n    class Meta:\n"
                    f"        database = db\n")
        f.write(f"\n\ndef create_tables():\n"
                f"    with db:\n"
                f"        db.create_tables([{titles_string}])\n"
                f"    return True\n"
                f"\n\nres = create_tables()\n")
    # create table in database
    exec(f"from create_model_{database_name} import res")
    exec(f"from create_model_{database_name} import {titles_string[0:-2]}")
    for sheet in data["sheets"]:
        title = sheet["properties"]["title"]
        data_sheet = service.spreadsheets().get(spreadsheetId=GOOGLE_SHEETS_ID, ranges=title,
                                                includeGridData=True).execute()
        field_names = []
        for name in data_sheet["sheets"][0]["data"][0]["rowData"][0]["values"]:
            field_names.append(name["userEnteredValue"]["stringValue"])
        for row in data_sheet["sheets"][0]["data"][0]["rowData"][1:]:
            i = 0
            s_arr = []
            for item in row["values"]:
                type_field = list(data_sheet["sheets"][0]["data"][0]["rowData"][1]["values"][i]["userEnteredValue"].keys())[0]
                if type_field == "numberValue":
                    s_arr.append(f"{field_names[i]}={item['formattedValue']}")
                else:
                    s_arr.append(f"{field_names[i]}='{item['formattedValue']}'")
                i += 1
            s = ""
            for i in s_arr:
                s = s + f"{i}" + ","
            print(s)
            exec(f"{title}.create({s})")

exel_to_db()
