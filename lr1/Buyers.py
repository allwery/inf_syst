import re

class Buyer:
    @staticmethod
    def validate_field(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            raise ValueError(f"Поле '{field_name}' должно быть типа {expected_type.__name__}.")
        if expected_type is str and not field_value.strip():
            raise ValueError(f"Поле '{field_name}' не может быть пустым.")
        if expected_type is str and not field_value.isalpha() and field_name in ["Имя", "Контактное лицо"]:
            raise ValueError(f"Поле '{field_name}' должно содержать только буквы.")
        if expected_type is str and field_name == "Телефон" and not re.match(r"^\+\d+$", field_value):
            raise ValueError(f"Поле '{field_name}' должно начинаться с '+' и содержать только цифры.")


    def __init__(self, *args):
        if len(args) == 5:  # Обычный вызов конструктора
            self._validate_and_set(*args)
        elif len(args) == 1 and isinstance(args[0], str):  # Строка
            self._from_string(args[0])
        elif len(args) == 1 and isinstance(args[0], dict):  # Словарь
            self._from_dict(args[0])
        else:
            raise ValueError("Неверные аргументы конструктора.")

    def _validate_and_set(self, id, name, address, phone, contact):
        self.validate_field("ID", id, int)
        self.validate_field("Имя", name, str)
        self.validate_field("Адрес", address, str)
        self.validate_field("Телефон", phone, str)
        self.validate_field("Контактное лицо", contact, str)

        self._id = id
        self._name = name
        self._address = address
        self._phone = phone
        self._contact = contact

    def _from_string(self, data_string):
        try:
            parts = data_string.split(';')
            if len(parts) != 5:
                raise ValueError("Неправильный формат строки. Необходимо 5 значений, разделенных точкой с запятой.")
            id, name, address, phone, contact = parts
            self._validate_and_set(int(id), name, address, phone, contact)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Ошибка разбора строки: {e}")

    def _from_dict(self, data_dict):
        try:
            id = int(data_dict['ID'])
            name = data_dict['Имя']
            address = data_dict['Адрес']
            phone = data_dict['Телефон']
            contact = data_dict['Контактное лицо']
            self._validate_and_set(id, name, address, phone, contact)
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка разбора словаря: {e}")


    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    def set_phone(self, phone):
        return self._phone

    def get_phone(self):
        return self._phone

    def get_contact(self):
        return self._contact

    def set_contact(self, contact):
       self._contact = contact

    def __str__(self):
        return f"Buyer(ID ={self._id}, Имя ='{self._name}', Адрес ='{self._address}', Телефон ='{self._phone}', Контакт ='{self._contact}')"


try:
    buyer1 = Buyer(1, "Ваня", "Ленина 1", "+777777777", "Ванек")
    print(buyer1)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer2 = Buyer("2;Леша;Пушкина 1;+88888888;Леха")
    print(buyer2)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer3 = Buyer({'ID': 3, 'Имя': 'Димон', 'Адрес': 'Дружбы 1', 'Телефон': '+77777777', 'Контактное лицо': 'Димас'})
    print(buyer3)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer4 = Buyer("1; ;Ленина 1;+777777777;Ванек") # Проверка на пустое имя
    print(buyer4)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer5 = Buyer("1;Ванькович;Ленина 1;777777777;Ванек") # Проверка телефона без +
    print(buyer5)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer6 = Buyer({'ID': 3, 'Имя': '123', 'Адрес': 'Дружбы 1', 'Телефон': '+77777777', 'Контактное лицо': 'Димас'}) #Проверка имени с цифрами
    print(buyer6)
except ValueError as e:
    print(f"Ошибка: {e}")
