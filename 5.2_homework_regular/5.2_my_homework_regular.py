# -*- coding: utf-8 -*-

import csv
import re
from pprint import pprint
# открыть и прочитать, сохранить в списк - contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # print("contacts_list", contacts_list)

# привести телефоны к корректному виду
def normalize_phone(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(?:\s*(доб\.)\s*(\d+))?"
    substitution = r"+7(\2)\3-\4-\5 \6\7"
    return re.sub(pattern, substitution, phone).strip()

# Обработка контактов
normalized_contacts = {}
for contact in contacts_list:
    # Объединить фио и разбиваем на части
    full_name = " ".join(contact[:3]).split()
    # print("full_name", full_name)
    # пересобираем фио
    last_name, first_name, *surname = (full_name + [""])[:3]
    surname = surname[0]

    # преобразовываем телефон
    phone = normalize_phone(contact[5])
    # print("телефон", phone)

    # ключ по которому объединим дубликаты
    key = (last_name, first_name)
    # print("ключ", key)

    # если уже есть -обновим
    if key in normalized_contacts:
        existing = normalized_contacts[key]
        # print("existing", existing)
        existing[2] = existing[2] or surname
        existing[3] = existing[3] or contact[3]
        existing[4] = existing[4] or contact[4]
        existing[5] = existing[5] or phone
        existing[6] = existing[6] or contact[6]
    else:
        # иначе- создадим
        normalized_contacts[key] = [last_name, first_name, surname, contact[3], contact[4], phone, contact[6]]
# print("пересобранный контакт:", normalized_contacts)
# пересобираем список для csv
final_contacts_list = list(normalized_contacts.values())
# print("final_contacts_list", final_contacts_list)
# Сохраняем final_contacts_list в новый csv
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)
