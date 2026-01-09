import json
import os
from typing import Any

import pandas as pd


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


def write_data_excel(path_dir, data: list[dict[str, Any]]) -> None:
    pathfile = os.path.join(os.path.dirname(__file__), path_dir, "survey_report.xlsx")
    with pd.ExcelWriter(pathfile) as writer:
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name="survey_report", index=False)


def data_processing(data: list[dict]) -> list[dict]:
    temp_data = []
    for item in data:
        temp_data_dict = {}
        temp_data_dict["Имя ПК"] = item["hostname"]
        temp_data_dict["Домен"] = item["domain"]
        temp_tech = item["tech"]
        temp_os = temp_tech["os"]["linux"]
        temp_data_dict["Операционная система"] = (
            f"ОС - {temp_os['name']}\n" f'Версия - {temp_os["version"]}\n' f"Ядро - {temp_os['kernel']}"
        )
        temp_data_dict["Процессор"] = temp_tech["cpu"][0]
        temp_data_dict["Видеоадаптер"] = temp_tech["videoadapter"][0]
        temp_data_dict["Материнская плата"] = (
            f"Вендор - {temp_tech['motherboard']['vendor']}\n" f'Модель - {temp_tech['motherboard']["model"]}'
        )
        temp_data_dict["Оперативная память"] = temp_tech["ram"]
        temp_disks = ""
        for_disk = temp_tech["disk"]
        for item_disk in for_disk:
            if item_disk["model"] == "unknown":
                continue
            else:
                temp_disks += (
                    f'Модель - {item_disk["model"]}\n'
                    f'Размер - {item_disk["size"]}\n'
                    f'Тип - {item_disk["storage_type"]}\n'
                )
                temp_disks += "Cъёмный\n" if item_disk["is_removable"] else "Не съёмный\n"
        temp_data_dict["Носители"] = temp_disks[: len(temp_disks) - 1]
        temp_data_dict["Монитор"] = item["per"]["monitor"]
        temp_lan = ""
        for item_lan in item["interfaces"]:
            temp_lan += (
                f'Имя - {item_lan["name"]}\n'
                f'IP-адрес {item_lan["ips"][0]['address']}\n'
                f'Подсеть - {item_lan["ips"][0]['subnet']}\n'
                f'MAC-адрес - {item_lan["mac"]}\n'
            )
            temp_lan += "Активен\n" if item_lan["is_active"] else "Не активен\n"
        temp_data_dict["Сетевой интерфейс"] = temp_lan[: len(temp_lan) - 1]
        temp_data.append(temp_data_dict)
        temp_data_dict["ID ПК"] = item["host_id"]

    return temp_data


def user_interface() -> str:
    path = input("Введите путь к файлам опроса в формате json: ")
    if len(path) == 0:
        return "data"
    else:
        return path


if __name__ == "__main__":
    path_file = user_interface()
    data_survey_report = load_data_json(path_file)
    data = data_processing(data_survey_report)
    write_data_excel(path_file, data)
