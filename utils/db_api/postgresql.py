# async def add_user(self, full_name, username, telegram_id):
#     sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
#     return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)
#
#
# async def select_all_users(self):
#     sql = "SELECT * FROM Users"
#     return await self.execute(sql, fetch=True)
#
#
# async def select_user(self, **kwargs):
#     sql = "SELECT * FROM Users WHERE "
#     sql, parameters = self.format_args(sql, parameters=kwargs)
#     return await self.execute(sql, *parameters, fetchrow=True)
#
#
# async def count_users(self):
#     sql = "SELECT COUNT(*) FROM Users"
#     return await self.execute(sql, fetchval=True)
#
#
# async def update_user_username(self, username, telegram_id):
#     sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
#     return await self.execute(sql, username, telegram_id, execute=True)
#
#
# async def delete_users(self):
#     await self.execute("DELETE FROM Users WHERE TRUE", execute=True)
#
#
# async def drop_users(self):
#     await self.execute("DROP TABLE Users", execute=True)

from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def create_product(self, name, category_id, photo_url, price, description):
        sql = "INSERT INTO Products (name, category_id, photo, price, description) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, name, category_id, photo_url, price, description, fetchrow=True)

    async def select_products(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def search_products_by_title(self, word):
        sql = "SELECT * FROM Products WHERE name ILIKE $1"
        word_with_wildcards = f"%{word}%"  # Add wildcard characters around the word
        return await self.execute(sql, word_with_wildcards, fetch=True)

        async with self.pool.acquire() as connection:
            connection: Connection
            products = await connection.fetch(sql, word_with_wildcards)
        return products

    async def delete_product(self, id):
        sql = "DELETE FROM Products WHERE id = $1"
        result = None  # Define and assign a default value to result
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                result = await connection.execute(sql, id)
        return result

    async def update_product(self, id, name, category_id, price, photo, description):
        sql = "UPDATE Products SET name=$2, category_id=$3, price=$4, photo=$5, description=$6 WHERE id=$1"
        return await self.execute(sql, id, name, category_id, price, photo, description, execute=True)

    async def create_category(self, title):
        sql = "INSERT INTO Categories (title) VALUES($1) returning *"
        return await self.execute(sql, title, fetchrow=True)

    async def select_categories(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def get_categories(self):
        sql = "SELECT * FROM Categories"
        return await self.execute(sql, fetch=True)

    # async def create_price(self, label, price):
    #     sql = "INSERT INTO Prices (label, price) VALUES($1, $2) returning *"
    #     return await self.execute(sql, label, price, fetchrow=True)
    #
    # async def select_prices(self, **kwargs):
    #     sql = "SELECT * FROM Prices WHERE "
    #     sql, parameters = self.format_args(sql, parameters=kwargs)
    #     return await self.execute(sql, *parameters, fetch=True)

    async def select_orders(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def create_order(self, user_id=None, currency=None, total_amount=None, invoice_payload=None,
                           state=None, city=None,
                           user_name=None, phone_number=None, email=None
                           ):
        sql = """INSERT INTO Orders (user_id, currency, total_amount, invoice_payload, state, city,
        user_name, phone_number, email) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning * """

        return await self.execute(sql, user_id, currency, total_amount, invoice_payload, state, city,
                                  user_name, phone_number, email, fetchrow=True)

    async def select_order_product(self, **kwargs):
        sql = "SELECT * FROM orders_products WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def create_order_product(self, order_id, product_id):
        sql = "INSERT INTO orders_products (order_id, product_id) VALUES($1, $2) returning *"
        return await self.execute(sql, order_id, product_id, fetchrow=True)
