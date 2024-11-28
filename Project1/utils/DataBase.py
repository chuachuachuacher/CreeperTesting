import asyncio
import aiomysql
from contextlib import asynccontextmanager

class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None

    async def create_pool(self): # 创建连接池
        try:
            self.pool = await aiomysql.create_pool(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                db=self.config['db'],
                charset=self.config['charset'],
                autocommit=self.config['autocommit'],
                maxsize=self.config['maxsize'],
                minsize=self.config['minsize'],
            )
            print('Mariadb连接成功——————————')
        except Exception as e:
            print(f"Failed to create pool: {e}")
            self.pool = None
    async def close_pool(self):
        if self.pool is not None:
            await self.pool.close()
            print("连接池关闭——————————")
        else:
            print("——————————连接池None")
    @asynccontextmanager
    async def get_connection(self):
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            self.pool.release(conn)

    async def query(self, sql, params=None):
        async with self.get_connection() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql, params)
                return await cursor.fetchall()

    async def execute(self, sql, params=None):
        async with self.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, params)
                if cursor.description:
                    return await cursor.fetchall()
                else:
                    return cursor.rowcount
        print("执行完毕——————————")

async def main():
    config = {
        'host': '192.168.150.20',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'Creepers',
        'charset': 'utf8',
        'autocommit': True,
        'maxsize': 10,
        'minsize': 1,
    }
    db = Database(config)
    await db.create_pool()

    
    affected_rows = await db.execute("create table if not exists %s (id int primary key, name varchar(50))", ('test'))
    print(f"Affected rows: {affected_rows}")

    await db.close_pool()

if __name__ == '__main__':
    asyncio.run(main())