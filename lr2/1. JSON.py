import json
import os
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
            self._from_json(args[0])
        elif len(args) == 1 and isinstance(args[0], Buyer):
            self._from_buyer(args[0])
        else:
            raise ValueError("Неверные аргументы для конструктора.")

    def _validate_and_set(self, id, name, address, phone, contact): 
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

    def _from_json(self, json_string):
        try:
            data = json.loads(json_string)
            id = int(data['ID'])
            name = data['Имя']
            address = data['Адрес']
            phone = data['Телефон']
            contact = data['Контакт']
            self._validate_and_set(id, name, address, phone, contact)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Ошибка при разборе JSON: {e}")

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


class Buyer_rep_json:
    def __init__(self, filepath="buyers.json"):
        self.filepath = filepath
        self.buyers = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_from_json()


    def load_from_json(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    self.buyers.append(Buyer(*item.values()))
                self.next_id = max(b._id for b in self.buyers) + 1 if self.buyers else 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке из JSON: {e}")


    def save_to_json(self):
        try:
            data = [vars(b) for b in self.buyers]
            with open(self.filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при сохранении в JSON: {e}")


    def get_buyer_by_id(self, buyer_id):
        for buyer in self.buyers:
            if buyer._id == buyer_id:
                return buyer
        return None


    def get_k_n_short_list(self, k, n):
        return [BuyerShort(b) for b in self.buyers[k-1:k+n]]


    def sort_by_field(self, field):
        try:
            self.buyers.sort(key=lambda x: getattr(x, f"_{field}"), reverse=False)
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def add_buyer(self, name, address, phone, contact):
        new_buyer = Buyer(self.next_id, name, address, phone, contact)
        self.buyers.append(new_buyer)
        self.next_id += 1
        self.save_to_json()
        return new_buyer

    def replace_buyer(self, buyer_id, name, address, phone, contact):
        buyer = self.get_buyer_by_id(buyer_id)
        if buyer:
            buyer._name = name
            buyer._address = address
            buyer._phone = phone
            buyer._contact = contact
            self.save_to_json()
            return True
        return False

    def delete_buyer(self, buyer_id):
        self.buyers = [b for b in self.buyers if b._id != buyer_id]
        self.save_to_json()

    def get_count(self):
        return len(self.buyers)


def main():
    buyer_rep = Buyer_rep_json()
    while True:
        print("\nМеню:")
        print("1. Вывести всех покупателей")
        print("2. Добавить покупателя")
        print("3. Удалить покупателя")
        print("4. Изменить данные покупателя")
        print("5. Найти покупателя по ID")
        print("6. Получить k-n короткий список")
        print("7. Отсортировать покупателей")
        print("8. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print("\nВсе покупатели:")
                for buyer in buyer_rep.buyers:
                    print(buyer)
            elif choice == "2":
                name = input("Введите имя: ")
                address = input("Введите адрес: ")
                phone = input("Введите телефон: ")
                contact = input("Введите контактное лицо: ")
                buyer_rep.add_buyer(name, address, phone, contact)
                print("Покупатель добавлен")
            elif choice == "3":
                buyer_id = int(input("Введите ID покупателя для удаления: "))
                if buyer_rep.delete_buyer(buyer_id):
                    print("Покупатель удален")
                else:
                    print("Готово")
            elif choice == "4":
                buyer_id = int(input("Введите ID покупателя для изменения: "))
                buyer = buyer_rep.get_buyer_by_id(buyer_id)
                if buyer:
                    buyer._name = input(f"Новое имя ({buyer._name}): ") or buyer._name
                    buyer._address = input(f"Новый адрес ({buyer._address}): ") or buyer._address
                    buyer._phone = input(f"Новый телефон ({buyer._phone}): ") or buyer._phone
                    buyer._contact = input(f"Новый контакт ({buyer._contact}): ") or buyer._contact
                    buyer_rep.save_to_json()
                    print("Данные покупателя изменены")
                else:
                    print("Покупатель не найден")
            elif choice == "5":
                buyer_id = int(input("Введите ID покупателя: "))
                buyer = buyer_rep.get_buyer_by_id(buyer_id)
                if buyer:
                    print("\nНайденный покупатель:", buyer)
                else:
                    print("Покупатель не найден.")
            elif choice == "6":
                k = int(input("Введите начальный элемент (k): "))
                n = int(input("Введите сколько взять (n): "))
                short_list = buyer_rep.get_k_n_short_list(k, n)
                print("\nКраткая информация о покупателях:", short_list)
            elif choice == "7":
                field = input("Введите поле для сортировки (ID, name, address, phone, contact): ")
                buyer_rep.sort_by_field(field)
                print("\nОтсортированный список:", buyer_rep.buyers)
            elif choice == "8":
                print("Выход")
                break
            else:
                print("Неверный выбор")
        except ValueError:
            print("Ошибка ввода данных. Пожалуйста, введите корректные значения")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
