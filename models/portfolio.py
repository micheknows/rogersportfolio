import mysql.connector
from mysql.connector import Error

import mysql.connector

class PortfolioItem:
    def __init__(self, id, title, short_desc, long_desc, image, demo_link, github_link):
        self.id = id
        self.title = title
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.image = image
        self.demo_link = demo_link
        self.github_link = github_link

class PortfolioItemDB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="micheknows",
            password="ph0nics3",
            database="portfolio"
        )

    def get_all_items(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, title, short_desc, image, demo_link, github_link FROM items")
        items = []
        for (id, title, short_desc, image, demo_link, github_link) in cursor:
            item = PortfolioItem(id=id, title=title, short_desc=short_desc, long_desc=None, image=image, demo_link=demo_link, github_link=github_link)
            items.append(item)
        cursor.close()
        return items


class PortfolioDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="micheknows",
            password="ph0nics3",
            database="portfolio"
        )

    def create(self, item):
        cursor = self.connection.cursor()
        sql = "INSERT INTO items (title, short_desc, long_desc, image, demo_link, github_link) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (item.title, item.short_desc, item.long_desc, item.image, item.demo_link, item.github_link)
        cursor.execute(sql, val)
        self.connection.commit()
        return cursor.lastrowid

    def read(self, id):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM items WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row is None:
            return None
        return PortfolioItem(row[1], row[2], row[3], row[4], row[5], row[6])

    def read_all(self):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM items"
        cursor.execute(sql)
        rows = cursor.fetchall()
        items = []
        for row in rows:
            item = PortfolioItem(row[1], row[2], row[3], row[4], row[5], row[6])
            item.id = row[0]
            items.append(item)
        return items

    def update(self, item):
        cursor = self.connection.cursor()
        sql = "UPDATE items SET title = %s, short_desc = %s, long_desc = %s, image = %s, demo_link = %s, github_link = %s WHERE id = %s"
        val = (item.title, item.short_desc, item.long_desc, item.image, item.demo_link, item.github_link, item.id)
        cursor.execute(sql, val)
        self.connection.commit()

    def delete(self, id):
        cursor = self.connection.cursor()
        sql = "DELETE FROM items WHERE id = %s"
        val = (id, )
        cursor.execute(sql, val)
        self.connection.commit()
