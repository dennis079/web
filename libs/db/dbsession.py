#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy as np
import pymysql
import tushare as ts
import easyquotation

# link to server
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'dmm'
USERNAME = 'root'
PASSWORD = 'qwer1234'
# DB_URI format ：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD,
                                                              HOSTNAME,
                                                              PORT,
                                                              DATABASE
                                                              )


# 1 create engine engine
engine = create_engine(DB_URI, echo=False)
# 2sessionmaker gennerate session class
Session = sessionmaker(bind=engine, expire_on_commit=False)
# 3 implement a session
dbSession = Session()
# 4create a base class
Base = declarative_base(engine)

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

ts.set_token("5359795e79c8dc5c26f8799f0f8be8b9cad8b9e083c0fb7b30f73755")
pro = ts.pro_api()

tcal = pro.trade_cal(exchange='SSE')

eq = easyquotation.use('qq') # some chinese company xinlang ['sina'] tengxun ['tencent', 'qq'] jisilu 'jsl'


# quotation.real('162411')

# quotation.stocks(['000001', '162411'])

# jsl = easyquotation.use('jsl') # ['jsl']
# jsl.funda()
# jsl.fundb()

# jsl.fundarb(jsl_username, jsl_password, avolume=100, bvolume=100, ptype='price')

# jsl.etfindex(index_id="", min_volume=0, max_discount=None, min_discount=None)


# quotation = easyquotation.use("timekline")
# data = quotation.real(['603828'], prefix=True)

# quotation = easyquotation.use("daykline")
# data = quotation.real(['00001','00700'])

# quotation = easyquotation.use("hkquote")
# data = quotation.real(['00001','00700'])

# not finished yet
class YYDatabaseConnector(object):
    engine = None
    Session = None

    def __init__(self):
        self.connect()

    def connect(self):
        if self.engine is None:
            self.engine = create_engine(DB_URI, echo=False, pool_size=100, pool_recycle=3600)

        if self.Session is None:
            self.Session = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))

    def get_session(self):
        self.connect()
        return self.Session()

    def close(self):
        self.Session.remove()