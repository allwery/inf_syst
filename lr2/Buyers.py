import yaml
import os
import json
import psycopg2
import re


class Buyer:
    @staticmethod
    def validate(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            print(f"Поле '{field_name}' должно быть типа {expected_type}.")
            return False
        if expected_type is str and not field_value:  
            print(f"Поле '{field_name}' не может быть пустым.")
            return False
        if expected_type is str and field_name == "Имя":
            if not re.fullmatch(r"[А-Яа-яЁё]+\s[А-Яа-яЁё]+", field_value):
                print(f"Поле '{field_name}' должно содержать имя и фамилию.")
                return False
        if expected_type is str and field_name == "Контактное лицо" and not field_value.isalpha():
            print(f"Поле '{field_name}' должно содержать только буквы.")
            return False
        if expected_type is str and field_name == "Телефон" and not re.match(r"^\+\d+$", field_value):
            print(f"Поле '{field_name}' должно начинаться с '+' и содержать только цифры.")
            return False
        return True

    def __init__(self, id, name, address, phone, contact):
        self._id = id
        if not Buyer.validate("Имя", name, str):
            raise ValueError("Некорректные данные")
        self._name = name
        if not Buyer.validate("Адрес", address, str):
            raise ValueError("Некорректные данные")
        self._address = address
        if not Buyer.validate("Телефон", phone, str):
            raise ValueError("Некорректные данные")
        self._phone = phone
        if not Buyer.validate("Контактное лицо", contact, str):
            raise ValueError("Некорректные данные")
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
        self._phone = phone

    def get_phone(self):
        return self._phone

    def get_contact(self):
        return self._contact

    def set_contact(self, contact):
        self._contact = contact

    def __str__(self):
        return (f"Buyer(ID={self._id},"
                f" Имя='{self._name}',"
                f" Адрес='{self._address}',"
                f" Телефон='{self._phone}',"
                f" Контактное лицо='{self._contact}')")

    def short_version(self):
        return f"Buyer ID: {self._id}, Имя: {self._name}"

    def __eq__(self, other):
        if not isinstance(other, Buyer):
            return False
        return self._id == other._id


class BuyerShort:
    def __init__(self, buyer):
        if not isinstance(buyer, Buyer):
            raise TypeError("Аргумент должен быть объектом класса Buyer.")
        self.id = buyer.get_id()
        name_parts = buyer.get_name().split()
        if len(name_parts) >= 2:
            self.name = name_parts[-1][0] + ". " + name_parts[0]
        else:
            self.name = buyer.get_name()
        self.phone = buyer.get_phone()

    def __str__(self):
        return f"BuyerShort(ID={self.id}, Имя={self.name}, Телефон={self.phone})"


class BuyerRep:
    def __init__(self, filepath=""):
        self.filepath = filepath
        self.buyers = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_data()

    def load_data(self):
        pass

    def save_data(self):
        pass

    def get_all_buyers(self):
        return self.buyers

    def add_buyer(self, name, address, phone, contact):
        new_buyer = Buyer(self.next_id, name, address, phone, contact)
        self.buyers.append(new_buyer)
        self.next_id += 1
        self.save_data()
        return True

    def delete_buyer(self, buyer_id):
        self.buyers = [b for b in self.buyers if b.get_id() != buyer_id]
        self.save_data()
        return True

    def get_buyer_by_id(self, buyer_id):
        for buyer in self.buyers:
            if buyer.get_id() == buyer_id:
                return buyer
        return None

    def get_k_n_short_list(self, k, n):
        return [BuyerShort(b) for b in self.buyers[k - 1:k + n - 1]]

    def sort_by_field(self, field):
        try:
            self.buyers.sort(key=lambda x: getattr(x, f"get_{field.lower()}")())
        except AttributeError:
            print(f"Поле '{field}' не найдено или у него нет геттера.")

    def get_count(self):
        return len(self.buyers)

    def replace_buyer(self, buyer_id, name, address, phone, contact):
        for i, buyer in enumerate(self.buyers):
            if buyer.get_id() == buyer_id:
                self.buyers[i] = Buyer(buyer_id, name, address, phone, contact)
                self.save_data()
                return True
        return False


class BuyerRepJSON(BuyerRep):
    def __init__(self, filepath="buyers.json"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    self.buyers.append(Buyer(*item.values()))
                self.next_id = max(b.get_id() for b in self.buyers) + 1 if self.buyers else 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке из JSON: {e}")

    def save_data(self):
        try:
            data = [vars(b) for b in self.buyers]
            with open(self.filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при сохранении в JSON: {e}")


class BuyerRepYAML(BuyerRep):
    def __init__(self, filepath="buyers.yaml"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    for buyer_data in data:
                        self.buyers.append(Buyer(*buyer_data.values()))
                    self.next_id = max(b.get_id() for b in self.buyers) + 1 if self.buyers else 1
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при загрузке из YAML: {e}")

    def save_data(self):
        try:
            data = [vars(b) for b in self.buyers]
            with open(self.filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при сохранении в YAML: {e}")


class DatabaseConnector:
    __instance = None

    @staticmethod
    def get_instance(host, user, password, database, port=5432):
        if DatabaseConnector.__instance is None:
            DatabaseConnector(host, user, password, database, port)
        return DatabaseConnector.__instance

    def __init__(self, host, user, password, database, port=5432):
        if DatabaseConnector.__instance is not None:
            raise Exception("Это паттерн 'Одиночка'")
        else:
            DatabaseConnector.__instance = self
            self.connection = None
            self.cursor = None
            try:
                self.connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port
                )
                self.cursor = self.connection.cursor()
            except psycopg2.Error as e:
                print(f"Ошибка подключения к базе данных PostgreSQL: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except psycopg2.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()


class BuyerRepDB:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def initialize_db(self):
        cursor = self.db_connector.execute_query("""
        CREATE TABLE IF NOT EXISTS Buyers (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL CHECK (Name ~* '^[а-яА-Яa-zA-Z\\s]+$'),
    Address TEXT NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE CHECK (Phone ~* '^\\+\\d+$'),
    Contact TEXT NOT NULL CHECK (Contact ~* '^[а-яА-Яa-zA-Z\\s]+$')
        );
        """)
        if cursor:
            print("База данных PostgreSQL и таблица 'Buyers' успешно созданы.")

    def get_buyer_by_id(self, buyer_id):
        cursor = self.db_connector.execute_query("SELECT * FROM Buyers WHERE ID = %s", (buyer_id,))
        if cursor:
            result = cursor.fetchone()
            if result:
                return Buyer(*result)
            else:
                return None
        return None

    def get_all_buyers(self):
        cursor = self.db_connector.execute_query("SELECT ID, Name, Address, Phone, Contact FROM Buyers")
        if cursor:
            results = cursor.fetchall()
            return [Buyer(row[0], row[1], row[2], row[3], row[4]) for row in results]
        return []

    def add_buyer(self, buyer: Buyer):
        if not isinstance(buyer, Buyer):
            raise TypeError("Аргумент должен быть объектом класса Buyer.")
        query = """INSERT INTO Buyers (Name, Address, Phone, Contact) 
                  VALUES (%s, %s, %s, %s) RETURNING ID;"""
        cursor = self.db_connector.execute_query(query, (buyer.get_name(),
                                                         buyer.get_address(),
                                                         buyer.get_phone(),
                                                         buyer.get_contact()))
        if cursor:
            result = cursor.fetchone()
            buyer.set_id(result[0])
            return buyer
        return None

    def replace_buyer(self, buyer: Buyer):
        if not isinstance(buyer, Buyer):
            raise TypeError("Аргумент должен быть объектом класса Buyer.")
        query = """UPDATE Buyers 
                  SET Name = %s, Address = %s, Phone = %s, Contact = %s 
                  WHERE ID = %s"""
        cursor = self.db_connector.execute_query(query, (buyer.get_name(),
                                                         buyer.get_address(),
                                                         buyer.get_phone(),
                                                         buyer.get_contact(),
                                                         buyer.get_id()))
        if cursor and cursor.rowcount > 0:
            print("Данные покупателя успешно обновлены.")
        else:
            print("Покупатель с таким ID не найден или данные не изменены.")

    def delete_buyer(self, buyer_id):
        try:
            cursor = self.db_connector.execute_query(
                "SELECT ID, Name, Address, Phone, Contact FROM Buyers WHERE ID > %s", (buyer_id,))
            if cursor is None:
                return False
            buyers_to_update = cursor.fetchall()

            cursor = self.db_connector.execute_query("DELETE FROM Buyers WHERE ID = %s", (buyer_id,))
            if cursor is None or cursor.rowcount == 0:
                print("Покупатель с таким ID не найден")
                return False

            for i, buyer_data in enumerate(buyers_to_update):
                new_id = buyer_data[0] - 1
                update_query = """UPDATE Buyers SET ID = %s WHERE ID = %s"""
                self.db_connector.execute_query(update_query, (new_id, buyer_data[0]))

            return True
        except Exception as e:
            print(f"Ошибка при удалении покупателя: {e}")
            return False

    def get_count(self):
        cursor = self.db_connector.execute_query("SELECT COUNT(*) FROM Buyers")
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else 0
        return 0

    def get_k_n_short_list(self, k, n):
        offset = k - 1
        limit = n
        cursor = self.db_connector.execute_query(
            "SELECT ID, Name, Address, Phone, Contact FROM Buyers LIMIT %s OFFSET %s", (limit, offset)
        )
        if cursor:
            results = cursor.fetchall()
            return [BuyerShort(Buyer(*row)) for row in results]
        return []


class BuyerRepDBAdapter(BuyerRep):
    def __init__(self, db_connector):
        super().__init__()
        self.db_rep = BuyerRepDB(db_connector)
        self.buyers = self.db_rep.get_all_buyers()
        self.next_id = self.db_rep.get_count() + 1 if self.db_rep.get_count() > 0 else 1

    def add_buyer(self, name, address, phone, contact):
        try:
            new_buyer = Buyer(self.next_id, name, address, phone, contact)
            added_buyer = self.db_rep.add_buyer(new_buyer)
            if added_buyer:
                self.buyers.append(added_buyer)
                self.next_id = self.db_rep.get_count() + 1
                return True
            return False
        except (psycopg2.Error, ValueError) as e:
            print(f"Ошибка при добавлении покупателя: {e}")
            return False

    def delete_buyer(self, buyer_id):
        result = self.db_rep.delete_buyer(buyer_id)
        self.buyers = self.db_rep.get_all_buyers()
        self.next_id = self.db_rep.get_count() + 1 if self.db_rep.get_count() > 0 else 1
        return result

    def get_buyer_by_id(self, buyer_id):
        buyer_data = self.db_rep.get_buyer_by_id(buyer_id)
        return buyer_data

    def get_all_buyers(self):
        return self.db_rep.get_all_buyers()

    def get_k_n_short_list(self, k, n):
        short_list_data = self.db_rep.get_k_n_short_list(k, n)
        return short_list_data

    def sort_by_field(self, field):
        buyers = self.get_all_buyers()
        try:
            buyers.sort(key=lambda x: getattr(x, f"_{field}"))
            self.buyers = buyers
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def replace_buyer(self, buyer_id, name, address, phone, contact):
        buyer = self.get_buyer_by_id(buyer_id)
        if buyer:
            buyer.set_name(name)
            buyer.set_address(address)
            buyer.set_phone(phone)
            buyer.set_contact(contact)
            self.db_rep.replace_buyer(buyer)
            self.buyers = self.db_rep.get_all_buyers()
            print("Данные покупателя изменены")
        else:
            print("Покупатель не найден")

    def get_count(self):
        return self.db_rep.get_count()

    def save_data(self):
        pass


def run_operations(buyer_rep):
    buyers = buyer_rep.get_all_buyers()
    while True:
        print("\nМеню:")
        print("1. Вывести всех покупателей")
        print("2. Добавить покупателя")
        print("3. Удалить покупателя")
        print("4. Изменить данные покупателя")
        print("5. Найти покупателя по ID")
        print("6. Получить k-n короткий список")
        print("7. Вывести кол-во покупателей")
        print("8. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print("\nВсе покупатели:")
                for buyer in buyers:
                    print(buyer)
            elif choice == "2":
                while True:
                    try:
                        name = input("Введите имя и фамилию: ")
                        address = input("Введите адрес: ")
                        phone = input("Введите телефон (начинающийся с +): ")
                        contact = input("Введите контактное лицо: ")
                        break
                    except ValueError as e:
                        print(f"Ошибка валидации: {e}")

                if buyer_rep.add_buyer(name, address, phone, contact):
                    buyers = buyer_rep.get_all_buyers()
                    print("Покупатель добавлен")
                else:
                    print("Ошибка при добавлении покупателя")
            elif choice == "3":
                buyer_id = int(input("Введите ID покупателя для удаления: "))
                if buyer_rep.delete_buyer(buyer_id):
                    buyers = buyer_rep.get_all_buyers()
                    print("Покупатель удален")
                else:
                    print("Покупатель не найден или ошибка при удалении")
            elif choice == "4":
                buyer_id = int(input("Введите ID покупателя для изменения: "))
                buyer = buyer_rep.get_buyer_by_id(buyer_id)
                if buyer:
                    name = input(f"Новое имя ({buyer.get_name()}): ") or buyer.get_name()
                    address = input(f"Новый адрес ({buyer.get_address()}): ") or buyer.get_address()
                    phone = input(f"Новый телефон ({buyer.get_phone()}): ") or buyer.get_phone()
                    contact = input(f"Новый контакт ({buyer.get_contact()}): ") or buyer.get_contact()
                    buyer_rep.replace_buyer(buyer_id, name, address, phone, contact)
                    buyers = buyer_rep.get_all_buyers()
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
                n = int(input("Введите количество элементов (n): "))
                short_list = buyer_rep.get_k_n_short_list(k, n)
                print("\nКраткая информация о покупателях:")
                for buyer in short_list:
                    print(str(buyer))
            elif choice == "7":
                count = buyer_rep.get_count()
                print(f"Количество покупателей: {count}")
            elif choice == "8":
                print("Выход")
                break
            else:
                print("Неверный выбор")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def run_prog():
    storage_type = input("Выберите тип хранилища (db, json, yaml): ")
    db_connector = None
    try:
        if storage_type == "db":
            host = 'localhost'
            user = 'postgres'
            password = 'vadimb'
            database = 'Buyers'
            db_connector = DatabaseConnector.get_instance(host, user, password, database)
            if db_connector.connection is None:
                print("Ошибка подключения к базе данных.")
                return
            buyer_rep = BuyerRepDBAdapter(db_connector)
            buyer_rep.db_rep.initialize_db()
        elif storage_type == "json":
            buyer_rep = BuyerRepJSON()
        elif storage_type == "yaml":
            buyer_rep = BuyerRepYAML()
        else:
            raise ValueError("Неподдерживаемый тип хранилища данных")
        run_operations(buyer_rep)
        if storage_type == "db" and db_connector:
            db_connector.close()
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    run_prog()
