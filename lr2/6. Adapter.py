import yaml
import os
import json
import psycopg2

class Buyer:
    @staticmethod
    def validate_field(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            raise ValueError(f"{field_name} тип должен быть {expected_type.__name__}.")
        if expected_type == str and not field_value.strip():
            raise ValueError(f"{field_name} не может быть пустой строкой.")

    def __init__(self, id, name, address, phone, contact):
        self._validate_and_set(id, name, address, phone, contact)


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


class BuyerShort:
    def __init__(self, buyer):
        self._id = buyer._id
        self._name = buyer._name
        self._phone = buyer._phone

    def __str__(self):
        return f"BuyerShort(ID={self._id}, Имя={self._name}, Телефон={self._phone})"


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
        self.buyers = [b for b in self.buyers if b._id != buyer_id]
        self.save_data()
        return True

    def get_buyer_by_id(self, buyer_id):
        for buyer in self.buyers:
            if buyer._id == buyer_id:
                return buyer
        return None

    def get_k_n_short_list(self, k, n):
        return [BuyerShort(b) for b in self.buyers[k - 1:k + n - 1]]

    def sort_by_field(self, field):
        try:
            self.buyers.sort(key=lambda x: getattr(x, f"_{field}"))
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def get_count(self):
        return len(self.buyers)

    def replace_buyer(self, buyer_id, name, address, phone, contact):
        for i, buyer in enumerate(self.buyers):
            if buyer._id == buyer_id:
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
                self.next_id = max(b._id for b in self.buyers) + 1 if self.buyers else 1
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
                    self.next_id = max(b._id for b in self.buyers) + 1 if self.buyers else 1
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
                Name VARCHAR(255) NOT NULL,
                Address TEXT NOT NULL,
                Phone VARCHAR(20) NOT NULL,
                Contact TEXT NOT NULL
            )
        """)
        if cursor:
            print("База данных PostgreSQL и таблица 'Buyers' успешно созданы.")

    def get_buyer_by_id(self, buyer_id):
        cursor = self.db_connector.execute_query("SELECT * FROM Buyers WHERE ID = %s", (buyer_id,))
        if cursor:
            result = cursor.fetchone()
            return dict(zip([desc[0] for desc in cursor.description], result)) if result else None
        return None

    def get_all_buyers(self):
        cursor = self.db_connector.execute_query("SELECT ID, Name, Address, Phone, Contact FROM Buyers") # Изменено
        if cursor:
            results = cursor.fetchall()
            return [dict(zip(['ID', 'Name', 'Address', 'Phone', 'Contact'], row)) for row in results] #Изменено
        return []

    def add_buyer(self, buyer_data):
        query = """INSERT INTO Buyers (Name, Address, Phone, Contact) 
                  VALUES (%s, %s, %s, %s) RETURNING ID;"""
        cursor = self.db_connector.execute_query(query, (buyer_data['Name'],
                                                         buyer_data['Address'],
                                                         buyer_data['Phone'],
                                                         buyer_data['Contact']))
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else None
        return None

    def replace_buyer(self, buyer_id, updated_buyer):
        query = """UPDATE Buyers 
                  SET Name = %s, Address = %s, Phone = %s, Contact = %s 
                  WHERE ID = %s"""
        self.db_connector.execute_query(query, (updated_buyer['Name'],
                                                updated_buyer['Address'],
                                                updated_buyer['Phone'],
                                                updated_buyer['Contact'],
                                                buyer_id))
        print("Данные покупателя успешно обновлены.")

    def delete_buyer(self, buyer_id):
        cursor = self.db_connector.execute_query("DELETE FROM Buyers WHERE ID = %s", (buyer_id,))
        return cursor is not None

    def get_count(self):
        cursor = self.db_connector.execute_query("SELECT COUNT(*) FROM Buyers")
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else 0
        return 0

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        cursor = self.db_connector.execute_query("SELECT Name, Address, Phone, Contact FROM Buyers LIMIT %s OFFSET %s", (n, offset))
        if cursor:
            results = cursor.fetchall()
            return [dict(zip(['Name', 'Address', 'Phone', 'Contact'], row)) for row in results]
        return []



class BuyerRepDBAdapter(BuyerRep):
    def __init__(self, db_connector):
        self.db_rep = BuyerRepDB(db_connector)
        self.buyers = self.db_rep.get_all_buyers()
        self.next_id = self.db_rep.get_count() + 1 if self.db_rep.get_count() > 0 else 1

    def add_buyer(self, name, address, phone, contact):
        buyer_data = {'Name': name, 'Address': address, 'Phone': phone, 'Contact': contact}
        new_id = self.db_rep.add_buyer(buyer_data)
        if new_id:
            self.buyers = self.db_rep.get_all_buyers()
            self.next_id += 1
            return True
        return False

    def delete_buyer(self, buyer_id):
        result = self.db_rep.delete_buyer(buyer_id)
        self.buyers = self.db_rep.get_all_buyers()
        return result

    def get_buyer_by_id(self, buyer_id):
        buyer_data = self.db_rep.get_buyer_by_id(buyer_id)
        if buyer_data:
            return Buyer(buyer_data['ID'], buyer_data['Name'], buyer_data['Address'], buyer_data['Phone'], buyer_data['Contact'])
        return None

    def get_all_buyers(self):
        return [Buyer(b['ID'], b['Name'], b['Address'], b['Phone'], b['Contact']) for b in self.db_rep.get_all_buyers()]

    def get_k_n_short_list(self, k, n):
        short_list_data = self.db_rep.get_k_n_short_list(k, n)
        return [BuyerShort(Buyer(0, b['Name'], b['Address'], b['Phone'], b['Contact'])) for b in short_list_data]

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
            buyer._name = name
            buyer._address = address
            buyer._phone = phone
            buyer._contact = contact
            self.db_rep.replace_buyer(buyer_id, {'Name': name, 'Address': address, 'Phone': phone,
                                                 'Contact': contact})
            self.buyers = self.db_rep.get_all_buyers()
            return True
        return False

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
                name = input("Введите имя: ")
                address = input("Введите адрес: ")
                phone = input("Введите телефон: ")
                contact = input("Введите контактное лицо: ")
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
                    name = input(f"Новое имя ({buyer._name}): ") or buyer._name
                    address = input(f"Новый адрес ({buyer._address}): ") or buyer._address
                    phone = input(f"Новый телефон ({buyer._phone}): ") or buyer._phone
                    contact = input(f"Новый контакт ({buyer._contact}): ") or buyer._contact
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
        except ValueError:
            print("Неверный формат ввода. Пожалуйста, введите число.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def main():
    storage_type = input("Выберите тип хранилища (db, json, yaml): ")

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
    main()
