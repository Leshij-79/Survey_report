import json
import os
from typing import Any


def load_data_json(path_dir: str) -> list[dict[str, Any]]:
    path_files = os.path.join(os.path.dirname(__file__), path_dir)
    list_files = os.listdir(path_files)
    data = []
    for file_name in list_files:
        path_file = os.path.join(path_files, file_name)
        try:
            with open(path_file, "r", encoding="utf-8") as json_file:
                data.append(json.load(json_file))
        except FileNotFoundError:
            return []
        except PermissionError:
            return []
        except TypeError:
            return []

    return data


def data_processing(data: list[dict]) -> list[dict]:
    temp_data =[]
    for item in data:
        temp_data_dict = {}
        temp_data_dict['Имя ПК'] = item['hostname']
        temp_data_dict['Домен'] = item['domain']
        temp_data_dict['ID ПК'] = item['host_id']
        temp_tech = item['tech']
        temp_os = temp_tech['os']['linux']
        temp_data_dict['Операционная система'] = (f'ОС - {temp_os['name']}\n'
                                                  f'Версия - {temp_os["version"]}\n'
                                                  f'Ядро - {temp_os['kernel']}')
        temp_data_dict['Процессор'] = temp_tech['cpu']
        temp_data_dict['Видеоадаптер'] = temp_tech['videoadapter']
        temp_data_dict['Материнская плата'] = (f'Вендор - {temp_tech['vendor']}\n'
                                               f'Модель - {temp_tech["model"]}')
        temp_data_dict['Оперативная память'] = temp_tech['ram']
        temp_disks = ''
        for item_disk in item['disk']:
            if item_disk['model'] == 'unknown':
                continue
            else:
                temp_disks += (f'Модель - {item_disk["model"]}\n'
                               f'Размер - {item_disk["size"]}\n'
                               f'Тип - {item_disk["storage_type"]}\n') + 'Не съёмный\n' if item_disk['is_removable'] \
                    else 'Съёмный\n'




def user_interface() -> str:
    path = input("Введите путь к файлам опроса в формате json: ")
    if len(path) == 0:
        return 'data'
    else:
        return path

if __name__ == "__main__":
    path_file = user_interface()
    data_survey_report = load_data_json(path_file)
    data = data_processing(data_survey_report)