import os
import psycopg2

from dotenv import load_dotenv
load_dotenv()

class Storage:

    MAX_BUFFER_LENGTH = 10
    TABLE_NAME = 'website_check'

    def __init__(self):
        self.buffer = []
        self.initfile = 'data/initdb.sql'
        self.dbconn = psycopg2.connect(os.getenv('DB_URI'))
        self._initdb()

    def _initdb(self):
        with open(self.initfile) as f:
            cursor = self.dbconn.cursor()
            sql = f.read()
            cursor.execute(sql)
            self.dbconn.commit()
            cursor.close()

    def store_message(self, message):
        if len(self.buffer) >= Storage.MAX_BUFFER_LENGTH:
            self.flush_buffer()
        self.buffer.append(message)

    def flush_buffer(self):
        sql = self._buffer2sql()
        if sql is not None:
            print(sql)
            self._execute_sql(sql)
        self.buffer = []

    def _buffer2sql(self):
        values = []
        for row in self.buffer:
            if all(e in row for e in ['url', 'time', 'code', 'content_check']):
                values.append(f"('{row['url']}', {row['code']}, {row['time']}, {row['content_check']})")
        if len(values):
            subquery = ', '.join(values)
            return f'INSERT INTO {Storage.TABLE_NAME} (url, http_code, response_time, content_check) VALUES {subquery};'
        return None

    def _execute_sql(self, sql):
        cursor = self.dbconn.cursor()
        cursor.execute(sql)
        self.dbconn.commit()
        cursor.close()

