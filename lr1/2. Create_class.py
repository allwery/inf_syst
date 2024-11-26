class Buyer:
  def __init__(self, id, name, address, phone, contact):
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


buyer1 = Buyer(1, "Ванек Ванькович", "Ленина 1", "+777777777", "Ванек")
print(buyer1) 