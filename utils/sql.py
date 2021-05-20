import MySQLdb
import os
import pandas as pd
import datetime as dt
from utils import DataFrameTools as dft
from dotenv import load_dotenv

load_dotenv()

username = 'admin'
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
db = os.getenv('db')
connect_timeout = 120
sql = 'select * from dbo.hospital_data'


def sql_results_to_df(sql, db, host, port=port, chunk=None, user=username, password=password):
    """

    :param sql:
    :param db:
    :param host:
    :param port:
    :param chunk:
    :param user:
    :param password:
    :return:
    """
    t1 = dt.datetime.now()
    with MySQLdb.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port,
        connect_timeout=120
    ) as conn:
        print('server: ' + host + ' DB: ' + db)
        print('SQL: ' + sql)
        cursor = conn.cursor()
        try:
            df: pd.DataFrame = pd.read_sql(sql, conn, chunksize=chunk)
            return df
        except:
            quit()
        t2 = dt.datetime.now()
        print('server: ' + host + ' DB: ' + db + ' RequestDuration: ' + str(t2 - t1))


def sql_commit(sql=None, db=db, host=host, port=port, chunk=None, user=username, password=password):
    """

    :param sql:
    :param db:
    :param host:
    :param port:
    :param chunk:
    :param user:
    :param password:
    :return:
    """
    with MySQLdb.connect(
        host=host,
            user=user,
            password=password,
            database=db,
            port=port,
            connect_timeout=120
    ) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
