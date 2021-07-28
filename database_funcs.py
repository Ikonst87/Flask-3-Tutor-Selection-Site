import json


def get_data_from_json(file_type):
    with open(f"data/{file_type}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def write_data_to_json(file_type, data):
    with open(f"data/{file_type}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        return 'success'
