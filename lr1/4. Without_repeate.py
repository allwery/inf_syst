class Buyer:
    @staticmethod
    def validate_field(f_name, f_value, ex_type):
        if not isinstance(f_value, ex_type):
            raise ValueError(f"{f_name} тип должен быть {ex_type.__name__}.")
        if ex_type == str and not f_value.strip():
            raise ValueError(f"{f_name} - не пустая строка")


    def __init__(self, id, name, address, phone, contact):
        Buyer.validate_field("id", id, int)
        Buyer.validate_field("name", name, str)
        Buyer.validate_field("address", address, str)
        Buyer.validate_field("phone", phone, str)
        Buyer.validate_field("contact", contact, str)

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

    def get_phone(self):
        return self._phone

    def set_phone(self, phone):
        self._phone = phone

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
    buyer2 = Buyer(2, "", "Пушкина 10", "+8888888888", "Леха") #Неправильное имя
    print(buyer2)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")

try:
    buyer3 = Buyer(3, 123, "Пушкина 10", "+8888888888", "Леха") #Неправильное имя
    print(buyer3)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")
