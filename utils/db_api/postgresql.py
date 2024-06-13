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

    async def create_user(self, first_name, telegram_user_id):
        sql = "INSERT INTO userlar_user (first_name, telegram_user_id) VALUES($1, $2) returning *"
        return await self.execute(sql, first_name, telegram_user_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM userlar_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_habar(self, telegram_user_id):
        sql = """
        SELECT m.id AS message_id, m.text, m.sent_at, u.id AS user_id, u.first_name, u.telegram_user_id
        FROM userlar_message m
        INNER JOIN userlar_user u ON m.user_id = u.id
        WHERE u.telegram_user_id = $1;
        """
        return await self.execute(sql, telegram_user_id, fetch=True)

