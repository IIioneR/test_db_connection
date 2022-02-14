import json
import os
from dotenv import load_dotenv
import psycopg2


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class PostgreSQL:
    def __init__(self, db_name, user, password, localhost):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.localhost = localhost

    def get_all_data(self):
        conn = psycopg2.connect(dbname=self.db_name, user=self.user,
                                password=self.password, host=self.localhost)
        cursor = conn.cursor()
        query = 'SELECT * FROM sessions'
        cursor.execute(query)
        records = cursor.fetchall()
        dic = {}
        stocks = []

        for session in records:
            dic['properties'] = {"type": session[1], "metric": "duration"}
            dic['value'] = session[2]
            dic['timestamp'] = session[3].timestamp()
            stocks.append(dic)
            data = (json.dumps(stocks, separators=(',', ':')))
        with open('output.json', 'w') as f:
            f.write(data)


psql_db = PostgreSQL(db_name=os.environ['DATABASE_NAME'],
                     user=os.environ['DATABASE_USER'],
                     password=os.environ['DATABASE_PASSWORD'],
                     localhost='localhost')

psql_db.get_all_data()
