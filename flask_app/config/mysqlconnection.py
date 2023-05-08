import pandas as pd
from sqlalchemy import create_engine
import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.engine = create_engine('mysql+pymysql://root:rootroot@localhost/' + db)

    def query_db(self, query, data=None):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(query, data)
                if query.lower().startswith("select"):
                    return [dict(row) for row in result]
                else:
                    return result.lastrowid
        except Exception as e:
            print("Something went wrong with a database interaction", e)
            return False

def connectToMySQL(db):
    return MySQLConnection(db)
