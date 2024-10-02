# db.py
import asyncpg
from typing import Optional

class Database:
    def __init__(self, port: str, user: str, password: str, database: str):
        self._host = 'db'
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host='db',
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
