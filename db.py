import sqlite3
from decimal import Decimal
from time import time

class BotDB:

    def __init__(self, db_file):
        # Инициализация соединения с бд
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        # Проверяем есть ли юзер в БД
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        # Получаем ид юзера в базе по ид в телеге
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def register_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))  
        return self.conn.commit()  

    def send_token_price(self, sol, ki, gene):
        self.cursor.execute("UPDATE `tokens` SET sol = ?, ki = ?, gene = ?", (sol, ki, gene,))
        return self.conn.commit()
    
    def get_token_price(self):
        result = self.cursor.execute("SELECT * FROM `tokens`")
        return result.fetchall()


    def close(self):
        # Закрытие соединения с БД
        self.conn.close()