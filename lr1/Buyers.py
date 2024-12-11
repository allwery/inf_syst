import re
class Buyer:
    @staticmethod
    def validate_data(name, address, phone, contact):
        if not isinstance(name, str) or not name.strip() or not name.isalpha():
            raise ValueError("Имя должно быть непустой строкой, содержащей только буквы.")
        if not isinstance(address, str):
            raise ValueError("Адрес должен быть непустой строкой.")
        if not isinstance(phone, str) or not re.match(r"^\+\d+$", phone):
            raise ValueError("Номер телефона должен начинаться с '+' и содержать только цифры.")
        if not isinstance(contact, str) or not contact.strip() or not contact.isalpha():
            raise ValueError("Контактное лицо должно быть непустой строкой, содержащей только буквы.")

    def __init__(self, id, name, address, phone, contact):
        Buyer.validate_data(name, address, phone, contact)

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
    buyer1 = Buyer(1, "Ванекк", "Ленина 1", "+777777777", "Ванек") #Всеправильно
    print(buyer1)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")

try:
    buyer2 = Buyer(2, "", "Пушкина 1", "+888888888", "123") #Неправильное имя и контакт
    print(buyer2)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")

try:
    buyer3 = Buyer(3, 123, "Пушкина 1", "888888888", "Леха") #Неправильное имя и телефон
    print(buyer3)
except ValueError as e:
    print(f"Ошибка создания покупателя: {e}")


buyer1 = Buyer(1, "Ванек Ванькович", "Ленина 1", "+777777777", "Ванек")
print(buyer1) 
