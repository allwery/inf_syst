class Buyer:
    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя - не пустая строка")

    @staticmethod
    def validate_address(address):
        if not isinstance(address, str):
            raise ValueError("Адрес - не пустая строка")

    @staticmethod
    def validate_phone(phone):
    # Можно добавить более строгую проверку формата телефона
        if not isinstance(phone, str):
          raise ValueError("Номер телефона - не пустая строка")

    @staticmethod
    def validate_contact(contact):
        if not isinstance(contact, str):
          raise ValueError("Контактное лицо - не пустая стрка")


    def __init__(self, id, name, address, phone, contact):
        Buyer.validate_name(name)
        Buyer.validate_address(address)
        Buyer.validate_phone(phone)
        Buyer.validate_contact(contact)

        self._id = id
        self._name = name
        self._address = address
        self._phone = phone
        self._contact = contact


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
    buyer1 = Buyer(1, "Ванек Ванькович", "Ленина 1", "+777777777", "Ванек") #Всеправильно
    print(buyer1)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")

try:
    buyer2 = Buyer(2, "", "Пушкина 1", "+888888888", "Леха") #Неправильное имя
    print(buyer2)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")

try:
    buyer3 = Buyer(3, 123, "Пушкина 1", "+888888888", "Леха") #Неправильное имя
    print(buyer3)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")
