import pymysql

class Database:
    def __init__(self, config):
        self.config = config

    def create_connection(self):
        try:
            conn = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                db=self.config['db'],
                charset=self.config['charset'],
                autocommit=self.config['autocommit']
            )
            print('MySQL连接成功——————————')
            return conn
        except Exception as e:
            print(f"Failed to create connection: {e}")
            return None

    def close_connection(self, conn):
        if conn:
            conn.close()
            print("连接关闭——————————")
        else:
            print("——————————连接None")

    def execute(self, sql, params=None):
        conn = self.create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    affected_rows = cursor.execute(sql, params)
                    conn.commit()  # 确保提交事务
                    return affected_rows
            except Exception as e:
                print(f"An error occurred: {e}")
                conn.rollback()  # 发生错误时回滚
                return None
            finally:
                self.close_connection(conn)
        else:
            print("无法创建数据库连接")
            return None

def main():
    config = {
        'host': '192.168.150.20',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'Creepers',
        'charset': 'utf8',
        'autocommit': True
    }
    db = Database(config)

    # 执行一个创建表的SQL语句，没有参数
    affected_rows = db.execute("CREATE TABLE IF NOT EXISTS test (id INT PRIMARY KEY, name VARCHAR(50))")
    print(f"受影响的行数: {affected_rows}")

    # 执行一个插入数据的SQL语句，有参数
    insert_sql = "INSERT INTO test (id, name) VALUES (%s, %s)"
    insert_params = (1, 'test_name')
    affected_rows = db.execute(insert_sql, insert_params)
    print(f"插入受影响的行数: {affected_rows}")

if __name__ == '__main__':
    main()