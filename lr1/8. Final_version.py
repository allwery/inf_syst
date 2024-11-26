class Buyer:
    @staticmethod
    def validate_field(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            raise ValueError(f"{field_name} тип должен быть {expected_type.__name__}.")
        if expected_type == str and not field_value.strip():
            raise ValueError(f"{field_name} не может быть пустой строкой.")

    def __init__(self, *args):
        if len(args) == 5:
            id, name, address, phone, contact = args
            self._validate_and_set(id, name, address, phone, contact)
        elif len(args) == 1 and isinstance(args[0], str):
            self._from_string(args[0])
        elif len(args) == 1 and isinstance(args[0], dict):
            self._from_dict(args[0])
        elif len(args) == 1 and isinstance(args[0], Buyer):
            self._from_buyer(args[0])
        else:
            raise ValueError("Неверные аргументы для конструктора.")

    def _validate_set(self, id, name, address, phone, contact):
        Buyer.validate_field("ID", id, int)
        Buyer.validate_field("Имя", name, str)
        Buyer.validate_field("Адрес", address, str)
        Buyer.validate_field("Телефон", phone, str)
        Buyer.validate_field("Контакт", contact, str)

        self._id = id
        self._name = name
        self._address = address
        self._phone = phone
        self._contact = contact

    def _from_string(self, data_string):
        try:
            parts = data_string.split(';')
            if len(parts) != 5:
                raise ValueError("Неверный формат строки.")
            id, name, address, phone, contact = parts
            self._validate_set(int(id), name, address, phone, contact)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Ошибка при разборе строки: {e}")

    def _from_dict(self, data_dict):
        try:
            id = int(data_dict['ID'])
            name = data_dict['Имя']
            address = data_dict['Адрес']
            phone = data_dict['Телефон']
            contact = data_dict['Контактная информация']
            self._validate_set(id, name, address, phone, contact)
        except (KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при разборе словаря: {e}")

    def _from_buyer(self, buyer):
        self._id = buyer._id
        self._name = buyer._name
        self._address = buyer._address
        self._phone = buyer._phone
        self._contact = buyer._contact

    def __str__(self):
        return f"Buyer(ID={self._id}, Имя='{self._name}', Адрес='{self._address}', Телефон='{self._phone}', Контакт='{self._contact}')"

    def __repr__(self):
        return f"Buyer(ID={self._id}, Имя='{self._name}')"

    def __eq__(self, other):
        if not isinstance(other, Buyer):
            return False
        return self._id == other._id

    def get_short(self):
        return BuyerShort(self)


class BuyerShort(Buyer):
    def __str__(self):
        return f"BuyerShort(ID={self._id}, Имя={self._name}, Телефон={self._phone})"


try:
    buyer = Buyer(1, "Ванек Ванькович", "Ленина 1", "+777777777", "Ванек")
    print(buyer)  # Полная инфа
    print(buyer.get_short())  # Краткая инфа
    
except ValueError as e:
  print(f"Error: {e}")
