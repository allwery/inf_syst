class Buyer:
  @staticmethod
  def validate_field(field_name, field_value, expected_type):
    if not isinstance(field_value, expected_type):
      raise ValueError(f"{field_name} тип должен быть {expected_type.__name__}.")
    if expected_type == str and not field_value.strip():
      raise ValueError(f"{field_name} - не пустая строка")


  def __init__(self, *args):
    if len(args) == 5: # обычный
      id, name, address, phone, contact = args
      self._validate_and_set(id, name, address, phone, contact)
    elif len(args) == 1 and isinstance(args[0], str): # строка
      self._from_string(args[0])
    elif len(args) == 1 and isinstance(args[0], dict): # слварь
      self._from_dict(args[0])
    else:
      raise ValueError(" неверные аргументы для конструктора")

  def _validate_set(self, id, name, address, phone, contact):
    Buyer.validate_field("ID", id, int)
    Buyer.validate_field("Имя", name, str)
    Buyer.validate_field("Адрес", address, str)
    Buyer.validate_field("Телефон", phone, str)
    Buyer.validate_field("Контактное лицо", contact, str)

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

  def _from_string(self, data_string): #если у нас формат строки ;__;__;__
    try:
      parts = data_string.split(';')
      if len(parts) != 5:
        raise ValueError("Неправильный формат тсроки")
      id, name, address, phone, contact = parts
      self._validate_set(int(id), name, address, phone, contact)
    except (ValueError, IndexError) as e:
      raise ValueError(f"Ошибка строки{e}")

  def _from_dict(self, data_dict): #для словаря
    try:
      id = int(data_dict['ID'])
      name = data_dict['Имя']
      address = data_dict['Адрес']
      phone = data_dict['Телефон']
      contact = data_dict['Контактное лицо']
      self._validate_set(id, name, address, phone, contact)
    except (KeyError, ValueError) as e:
      raise ValueError(f"Ошибка словаря {e}")

  def __str__(self):
    return f"Buyer(ID={self._id}, Имя='{self._name}', Адрес='{self._address}', Телефон='{self._phone}', Контактное лицо='{self._contact}')"

  def __repr__(self):  
    return f"Buyer(ID={self._id}, Имя='{self._name}')"

  def __eq__(self, other):
    if not isinstance(other, Buyer):
      return False
    return self._id == other._id

class BuyerShort:
  def __init__(self, buyer):
    if not isinstance(buyer, Buyer):
      raise TypeError("Коротка версия должна быть создана на основе длинной")
    self._id = buyer._id
    self._name = buyer._name
    self._phone = buyer._phone

  def __str__(self):
    return f"BuyerShort(ID={self._id}, Имя={self._name}, Телефон={self._phone})"
try: #обычный
  buyer1 = Buyer(1, "Ванек Ванькович", "Ленина 1", "+777777777", "Ванек")
  short_buyer = BuyerShort(buyer1)

  print(repr(buyer1))
  buyer_short = BuyerShort(Buyer("1;Ванек Ванькович;Ленина 1;+777777777;Ванек"))
  print(buyer_short)
except ValueError as e:
  print(f"Error: {e}")

try: #пробуем для формата ;__;__
  buyer2 = Buyer("1;Ванек Ванькович;Ленина 1;+777777777;Ванек")
  print(buyer2)
  print(repr(buyer2))
except ValueError as e:
  print(f"Error: {e}")

try: #для словаря
  buyer3 = Buyer(
    {'ID': 3, 'Имя': 'Димон', 'Адрес': 'Дружбы 1', 'Телефон': '+77777777', 'Контактное лицо': 'Димас'})
  print(buyer3)
  print(repr(buyer3))
except ValueError as e:
  print(f"Error: {e}")

print(buyer1 == buyer2)
print(buyer1 == buyer3)
