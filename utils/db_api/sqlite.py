import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path: str = 'test_bot.db'):
        self.db_path = db_path

    @property
    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table_users(self):
        cur = self.connect.cursor()
        try:
            cur.execute("""
                CREATE TABLE users(
                    id INT PRIMARY KEY NOT NULL, 
                    fullname VARCHAR(100) NOT NULL, 
                    phone VARCHAR(20) NOT NULL, 
                    email VARCHAR(50) NULL, 
                    birthday DATE NULL,
                    urinish INT DEFAULT 0 NULL
                    )
            """)
            print("Jadval yaratildi")
        except sqlite3.OperationalError as err:
            print(err)
        self.connect.close()

    def select_users(self):
        cur = self.connect.cursor()
        res = cur.execute("""
            SELECT * FROM users
        """)
        self.connect.close()
        return res.fetchall()

    def select_user(self, user_id):
        cur = self.connect.cursor()
        SQL = """
            SELECT * FROM users WHERE id=?
        """
        res = cur.execute(SQL, (user_id,))
        self.connect.close()
        return res.fetchone()

    def select_users_ids(self):
        cur = self.connect.cursor()
        res = cur.execute("""
            SELECT id FROM users
        """)
        ids = [set_obj[0] for set_obj in res.fetchall()]
        self.connect.close()
        return ids

    def add_user(self, id, fullname, phone, email=None, birthday=None, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            INSERT INTO users (id, fullname, phone, email, birthday)
            VALUES
            (?, ?, ?, ?, ?)
        """
        cur.execute(SQL, (id, fullname, phone, email, birthday))
        if commit:
            conn.commit()
            print("Bazaga user qo'shildi")
            conn.close()

    def add_email_birthday(self, id, email, birthday, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            UPDATE users SET email=?, birthday=? WHERE id=?
        """
        cur.execute(SQL, (email, birthday, id))
        if commit:
            conn.commit()
            print("To'liq ro'yxatdan o'tish")
            conn.close()

    def delete_users(self, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            DROP TABLE users
        """
        cur.execute(SQL)
        if commit:
            conn.commit()
            print("Foydalanuvchilar o'chirildi!")
            self.create_table_users()
            conn.close()

    def update_urinish(self, user_id, urinish, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET urinish=? WHERE id=?
                """
        cur.execute(SQL, (urinish, user_id))
        if commit:
            conn.commit()
            print("Urinish oshirildi!")
            conn.close()

    def update_email(self, user_id, email, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET email=? WHERE id=?
                """
        cur.execute(SQL, (email, user_id))
        if commit:
            conn.commit()
            print("Email o'zgartirildi!")
            conn.close()

    def update_number(self, user_id, number, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET phone=? WHERE id=?
                """
        cur.execute(SQL, (number, user_id))
        if commit:
            conn.commit()
            print("Telefon raqam o'zgartirildi!")
            conn.close()

    def update_birthday(self, user_id, birthday, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET birthday=? WHERE id=?
                """
        cur.execute(SQL, (birthday, user_id))
        if commit:
            conn.commit()
            print("Tug'ilgan kun o'zgartirildi!")
            conn.close()

    def update_fullname(self, user_id, fullname, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    UPDATE users SET fullname=? WHERE id=?
                """
        cur.execute(SQL, (fullname, user_id))
        if commit:
            conn.commit()
            print("Ism-familiya o'zgartirildi!")
            conn.close()

    def create_table_tests(self):
        cur = self.connect.cursor()
        try:
            cur.execute("""
                        CREATE TABLE tests(
                            question VARCHAR(500) NOT NULL, 
                            photo_id VARCHAR(100) NULL,
                            response VARCHAR(20) NOT NULL, 
                            response1 VARCHAR(20) NOT NULL, 
                            response2 VARCHAR(20) NOT NULL, 
                            response3 VARCHAR(20) NOT NULL, 
                            at_date TIMESTAMP NULL
                            )
                    """)
            print("Test jadvali yaratildi")
        except sqlite3.OperationalError as err:
            print(err)
        self.connect.close()

    def select_tests(self):
        cur = self.connect.cursor()
        res = cur.execute("""
                    SELECT * FROM tests
                """)
        self.connect.close()
        return res.fetchall()

    def select_count_tests(self):
        cur = self.connect.cursor()
        res = cur.execute("""
                            SELECT count(*) FROM tests
                        """)
        self.connect.close()
        return res.fetchone()[0]

    def add_test(self, question, response, response1, response2, response3, photo_id: str = None, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
                    INSERT INTO tests (question, photo_id, response, response1, response2, response3, at_date)
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?)
                """
        cur.execute(SQL, (question, photo_id, response, response1, response2, response3, f'{datetime.now()}'))
        if commit:
            conn.commit()
            print("Bazaga test qo'shildi")
            conn.close()

    def delete_test(self, question, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            DELETE FROM tests WHERE question=?
        """
        cur.execute(SQL, (question,))
        if commit:
            conn.commit()
            print("Test o'chirildi!")
            conn.close()

    def delete_tests(self, commit=True):
        conn = self.connect
        cur = conn.cursor()
        SQL = """
            DROP TABLE tests
        """
        cur.execute(SQL)
        if commit:
            conn.commit()
            self.create_table_tests()
            print("Testlar o'chirildi!")
            conn.close()


obj = Database()
# obj.delete_users()
# print(obj.create_table_users())
# obj.add_user(1, "wvgww", "sfvwegv")
# print(type(obj.select_users()[0][5]))
# print(obj.select_user(1)[5])