import sqlite3

conn = sqlite3.connect("prices.db")

cursor = conn.cursor() 


# com = """
# CREATE TABLE PRICES(
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     LINK TEXT NOT NULL,
#     STATUS TEXT NOT NULL,
#     PRICE INTEGER NOT NULL
# );
# """
# cursor.execute(com)


class DbHandler:
    INPUT = "INSERT INTO PRICES (LINK,STATUS, PRICE) VALUES (?, ?, ?)"
    LASTPRICE = "SELECT * FROM PRICES p WHERE id = (SELECT MAX(id) FROM PRICES WHERE link = p.link);"
    DELETE_LAST = "DELETE FROM PRICES WHERE link = ?"

    def __init__(self):
        self.conn = sqlite3.connect("prices.db")
        self.cursor = self.conn.cursor()

    def input_price(self, link, status, price):
        try:
            self.cursor.execute(self.INPUT, (link,status, price))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}")

    def get_last_price(self):
        try:
            self.cursor.execute(self.LASTPRICE)
            result = self.cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def delete(self,link):
        try:
            self.cursor.execute(self.DELETE_LAST, (link,))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Database error: {e}")

    def close(self):
        self.conn.close()