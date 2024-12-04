import mysql.connector

class BuyerRepDB:
    def __init__(self,
                 host,
                 user,
                 password,
                 database,
                 port = 3306):
        self.connection = None
        self.cursor = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port = port
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(f"Ошибка подключения к базе данных MySQL: {e}")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def initialize_db(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Buyers (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL,
                    Address TEXT NOT NULL,
                    Phone VARCHAR(20) NOT NULL,
                    Contact TEXT NOT NULL
                )
            """)
            self.connection.commit()
            print("База данных MySQL и таблица 'Buyers' успешно созданы.")
        except mysql.connector.Error as e:
            print(f"Ошибка создания таблицы: {e}")
            if self.connection:
                self.connection.rollback()

    def get_buyer_by_id(self, buyer_id):
        try:
            self.cursor.execute("SELECT * FROM Buyers WHERE ID = %s", (buyer_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as e:
            print(f"Ошибка получения покупателя по ID: {e}")
            return None

    def get_all_buyers(self):
        try:
            self.cursor.execute("SELECT * FROM Buyers")
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Ошибка получения всех покупателей: {e}")
            return []

    def add_buyer(self, buyer_data):
        try:
            query = """INSERT INTO Buyers (Name, Address, Phone, Contact) 
                      VALUES (%s, %s, %s, %s)"""
            self.cursor.execute(query, (buyer_data['Name'], buyer_data['Address'], buyer_data['Phone'], buyer_data['Contact']))
            self.connection.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Ошибка добавления покупателя: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def replace_buyer(self, buyer_id, updated_buyer):
        try:
            query = """UPDATE Buyers 
                      SET Name = %s, Address = %s, Phone = %s, Contact = %s 
                      WHERE ID = %s"""
            self.cursor.execute(query, (updated_buyer['Name'], updated_buyer['Address'], updated_buyer['Phone'], updated_buyer['Contact'], buyer_id))
            self.connection.commit()
            print("Данные покупателя успешно обновлены.")
        except mysql.connector.Error as e:
            print(f"Ошибка обновления покупателя: {e}")
            if self.connection:
                self.connection.rollback()

    def delete_buyer(self, buyer_id):
        try:
            self.cursor.execute("DELETE FROM Buyers WHERE ID = %s", (buyer_id,))
            self.connection.commit()
            return True #возвращает True если удаление прошло успешно
        except mysql.connector.Error as e:
            print(f"Ошибка удаления покупателя: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def get_count(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM Buyers")
            result = self.cursor.fetchone()
            return result['count'] if result else 0
        except mysql.connector.Error as e:
            print(f"Ошибка получения количества покупателей: {e}")
            return 0

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        try:
            self.cursor.execute("SELECT Name, Address, Phone, Contact FROM Buyers LIMIT %s OFFSET %s", (n, offset))
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            print(f"Ошибка получения списка покупателей: {e}")
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
                buyer_data = {
                    'Name': input("Введите имя: "),
                    'Address': input("Введите адрес: "),
                    'Phone': input("Введите телефон: "),
                    'Contact': input("Введите контактное лицо: ")
                }
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
    user = 'Vadim'
    password = 'vadimb10'
    database = 'Buyers'

    try:
        buyer_rep = BuyerRepDB(host, user, password, database)
        buyer_rep.initialize_db()

        while True:
            print("\nМеню:")
            print("1. Работа с базой данных")
            print("2. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                run_operations(buyer_rep)
            elif choice == "2":
                print("Выход...")
                break
            else:
                print("Неверный выбор.")

    except mysql.connector.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
    finally:
        if buyer_rep:
            buyer_rep.close()
            print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()
