import json

import data


def create_json_file(file_type, data):
    with open(f"data/{file_type}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        return 'success'


weekdays = dict(mon="Понедельник", tue="Вторник", wed="Среда", thu="Четверг", fri="Пятница", sat="Суббота",
                sun="Воскресенье")
free_time = {"1-2": "1-2 часа в неделю", "3-5": "3-5 часов в неделю", "5-7": "5-7 часов в неделю",
             "7-10": "7-10 часов в неделю"}
teachers_dict = {}
booking = []
request = []

for teacher in data.teachers:
    teachers_dict[teacher['id']] = teacher
for teacher in teachers_dict.values():
    del teacher["id"]

create_json_file("teachers", teachers_dict)
create_json_file("goals", data.goals)
create_json_file("weekdays", weekdays)
create_json_file("free_time", free_time)
create_json_file("booking", booking)
create_json_file("request", request)
