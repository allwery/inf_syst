import re

class Buyer:
    @staticmethod
    def validate_field(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            raise ValueError(f"Поле '{field_name}' должно быть типа {expected_type.__name__}.")
        if expected_type is str and not field_value.strip():
            raise ValueError(f"Поле '{field_name}' не может быть пустым.")
        if expected_type is str and field_name == "Имя":
            if not re.fullmatch(r"[А-Яа-яЁё]+\s[А-Яа-яЁё]+", field_value):
                raise ValueError(
                    f"Поле '{field_name}' должно содержать имя и фамилию, разделенные пробелом (только буквы).")
        if expected_type is str and not field_value.isalpha() and field_name == "Контактное лицо":
            raise ValueError(f"Поле '{field_name}' должно содержать только буквы.")
        if expected_type is str and field_name == "Телефон" and not re.match(r"^\+\d+$", field_value):
            raise ValueError(f"Поле '{field_name}' должно начинаться с '+' и содержать только цифры.")


    def __init__(self, *args):
        if len(args) == 5:  # Обычный вызов конструктора
            self._validate(*args)
        elif len(args) == 1 and isinstance(args[0], str):  # Строка
            self._from_string(args[0])
        elif len(args) == 1 and isinstance(args[0], dict):  # Словарь
            self._from_dict(args[0])
        else:
            raise ValueError("Неверные аргументы конструктора.")

    def _validate(self, id, name, address, phone, contact):
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
            self._validate(int(id), name, address, phone, contact)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Ошибка разбора строки: {e}")

    def _from_dict(self, data_dict):
        try:
            id = int(data_dict['ID'])
            name = data_dict['Имя']
            address = data_dict['Адрес']
            phone = data_dict['Телефон']
            contact = data_dict['Контактное лицо']
            self._validate(id, name, address, phone, contact)
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
        return f"Buyer(ID={self._id}, Имя='{self._name}', Адрес='{self._address}', Телефон='{self._phone}', Контактное лицо='{self._contact}')"

    def short_version(self):
        return f"Buyer ID: {self._id}, Имя: {self._name}"

    def __eq__(self, other):
        if not isinstance(other, Buyer):
            return False
        return (self._id, self._name, self._address, self._phone, self._contact) == \
            (other._id, other._name, other._address, other._phone, other._contact)


class ShortBuyer:
    def __init__(self, buyer):
        if not isinstance(buyer, Buyer):
            raise TypeError("Аргумент должен быть объектом класса Buyer.")
        self.id = buyer.get_id()
        name_parts = buyer.get_name().split()
        if len(name_parts) >=2:
          self.name = name_parts[-1][0] + ". " + name_parts[0]
        else:
          self.name = buyer.get_name()
        self.phone = buyer.get_phone()


    def __str__(self):
        return f"ShortBuyer(ID={self.id}, Имя='{self.name}', Телефон='{self.phone}')"

try:
    buyer = Buyer(1, "Иван Иванов", "Ленина 1", "+77777777", "Вася")
    short_buyer = ShortBuyer(buyer)
    print(buyer)
    print(short_buyer)
except ValueError as e:
    print(f"Ошибка: {e}")

try:
    buyer_err = Buyer(2, "Иванов", "Ленина 2", "+77777777", "Петя")
    short_buyer_err = ShortBuyer(buyer_err)
    print(buyer_err)
    print(short_buyer_err)
except ValueError as e:
    print(f"Ошибка: {e}")

print(f"buyer4 == buyer5: {buyer4 == buyer5}")  
print(f"buyer4 == buyer6: {buyer4 == buyer6}")  
