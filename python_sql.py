# Database API
# Expand previous Homework 5/6/7/8/9 with additional class, which allow to save records into database:
# 1.Different types of records require different data tables
# 2.New record creates new row in data table
# 3.Implement “no duplicate” check.


import os
import datetime
import pyodbc
from python_strings_hw import normalize_letter_case


class DBNewsSaver:
    def __init__(self, db_path=None):
        # Default database file path
        self.db_path = db_path or os.path.join(os.getcwd(), "news_database.db")

        # Connect to SQLite using ODBC driver
        self.conn = pyodbc.connect(f"DRIVER=SQLite3 ODBC Driver;Database={self.db_path};")

        # Create cursor
        self.cursor = self.conn.cursor()

        # Create required tables if not exist
        self._create_tables()

    def _create_tables(self):
        # Create table for News
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS News (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                city TEXT NOT NULL,
                publishing_datetime TEXT NOT NULL
            )
        """)
        # Create table for Private Ads
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Private_Ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                expiration_date TEXT NOT NULL,
                days_left INTEGER NOT NULL
            )
        """)
        # Create table for Horoscopes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Horoscopes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sign TEXT NOT NULL,
                message TEXT NOT NULL,
                horoscope_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

        # Duplicates check
    def _is_duplicate(self, table, conditions, values):
        """
        Check if a record already exists in the target table.
        :param table: Table name (string)
        :param conditions: SQL WHERE clause (string)
        :param values: Tuple of values to check
        :return: True if duplicate exists, False otherwise
        """
        query = f"SELECT COUNT(*) FROM {table} WHERE {conditions}"
        self.cursor.execute(query, values)
        return self.cursor.fetchone()[0] > 0

    def db_insert_news(self, text, city, publishing_datetime):
        text = normalize_letter_case(text)
        city = city.title()
        if self._is_duplicate("News", "text=? AND city=?", (text, city)):
            print("Duplicate News record skipped.")
            return
        self.cursor.execute(
            "INSERT INTO News (text, city, publishing_datetime) VALUES (?, ?, ?)",
            (text, city, publishing_datetime)
        )
        self.conn.commit()
        print("News record saved to DB.")

    def db_insert_private_ad(self, text, expiration_date, days_left):
        text = normalize_letter_case(text)
        if self._is_duplicate("Private_Ads", "text=? AND expiration_date=?", (text, expiration_date)):
            print("Duplicate Private Ad record skipped.")
            return
        self.cursor.execute(
            "INSERT INTO Private_Ads (text, expiration_date, days_left) VALUES (?, ?, ?)",
            (text, expiration_date, days_left)
        )
        self.conn.commit()
        print("Private Ad record saved to DB.")

    def db_insert_horoscope(self, sign, message, horoscope_date):
        message = normalize_letter_case(message)
        if self._is_duplicate("Horoscopes", "sign=? AND message=?", (sign, message)):
            print("Duplicate Horoscope record skipped.")
            return
        self.cursor.execute(
            "INSERT INTO Horoscopes (sign, message, horoscope_date) VALUES (?, ?, ?)",
            (sign, message, horoscope_date)
        )
        self.conn.commit()
        print("Horoscope record saved to DB.")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = DBNewsSaver()

#    # Test manual inserts
#    db.db_insert_news(
#        text="Local festival starts this weekend.",
#        city="Minsk",
#        publishing_datetime=datetime.datetime.now().isoformat(timespec="seconds")
#    )
#
#    db.db_insert_private_ad(
#        text="Selling a bicycle in good condition.",
#        expiration_date="2025-12-31",
#        days_left=(datetime.datetime.strptime("2025-12-31", "%Y-%m-%d") - datetime.datetime.now()).days
#    )
#
#    db.db_insert_horoscope(
#        sign="Leo",
#        message="Today is a great day for creativity.",
#        horoscope_date=datetime.datetime.now().strftime("%Y-%m-%d")
#    )
