import psycopg2
import re

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
                    Name VARCHAR(255) NOT NULL CHECK (Name ~* '^[а-яА-Яa-zA-Z\s]+$'),
                    Address TEXT NOT NULL,
                    Phone VARCHAR(20) NOT NULL UNIQUE CHECK (Phone ~* '^\+\d+$'),
                    Contact TEXT NOT NULL CHECK (Contact ~* '^[а-яА-Яa-zA-Z\s]+$')
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
        cursor = self.db_connector.execute_query("SELECT * FROM Buyers")
        if cursor:
            results = cursor.fetchall()
            return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
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
                    buyer_data = {
                        'Name': input("Введите имя и фамилию : "),
                        'Address': input("Введите адрес: "),
                        'Phone': input("Введите телефон (начинающийся с +): "),
                        'Contact': input("Введите контактное лицо : ")
                    }

                    if (re.fullmatch(r'^[а-яА-Яa-zA-Z\s]+$', buyer_data['Name']) and
                            re.fullmatch(r'^\+\d+$', buyer_data['Phone']) and
                            re.fullmatch(r'^[а-яА-Яa-zA-Z\s]+$', buyer_data['Contact'])):
                        break
                    else:
                        print("Неверный формат данных. Пожалуйста, повторите ввод.")

                if buyer_rep.add_buyer(buyer_data):
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
                    updated_buyer = {
                        'Name': input(f"Новое имя ({buyer['Name']}): ") or buyer['Name'],
                        'Address': input(f"Новый адрес ({buyer['Address']}): ") or buyer['Address'],
                        'Phone': input(f"Новый телефон ({buyer['Phone']}): ") or buyer['Phone'],
                        'Contact': input(f"Новый контакт ({buyer['Contact']}): ") or buyer['Contact']
                    }
                    buyer_rep.replace_buyer(buyer_id, updated_buyer)
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
                print("\nКраткая информация о покупателях:", short_list)
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
    host = 'localhost'
    user = 'postgres'
    password = 'vadimb'
    database = 'Buyers'

    db_connector = DatabaseConnector.get_instance(host, user, password, database)
    if db_connector.connection is None:
        print("Ошибка подключения к базе данных.")
        return

    buyer_rep = BuyerRepDB(db_connector)
    buyer_rep.initialize_db()
    run_operations(buyer_rep)
    db_connector.close()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
