#coding=utf-8

from libs.db.dbsession import Base, dbSession

import pymysql
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from libs.db.dbsession import engine
#from libs.db.dbsession import Base
from sqlalchemy import Column, Integer, String,Float

#initial SQLORM class，table will inherit it
#Base = declarative_base()
''' test part
class YYUser(Base):
    __tablename__ = 'dusers'  #yy_users for able user check

    uid = Column(Integer, primary_key=True)
    uname = Column(String(32))
    nickname = Column(String(32))
    wechat = Column(String(32))
    ustatus = Column(Integer)
    utype = Column(Integer)
    ulevel = Column(Integer)
    viplevel = Column(Integer)
    sparam = Column(String(32))
    nparam = Column(Integer)


    def __init__(self,uname,nickname,wechat,ustatus,utype,ulevel,viplevel,sparam,nparam):
        self.uname = uname
        self.nickname = nickname
        self.wechat = wechat
        self.ustatus = ustatus
        self.utype = utype
        self.ulevel = ulevel
        self.viplevel = viplevel
        self.sparam = sparam
        self.nparam = nparam
        self.uid = 0

    def __repr__(self):
        return "<YYUser(uname='%s',nickname='%s',viplevel='%d')>" % self.uname % self.nickname % self.viplevel
    
   
    
    '''


class YYUser(Base):
    __tablename__ = 'dusers'

    uid = Column(Integer, primary_key=True)
    uname = Column(String(32))
    utype = Column(Integer)
    sparam = Column(String(32))
    nparam = Column(Integer)

    def __init__(self, uname, nickname, wechat, ustatus, utype, ulevel, viplevel, sparam, nparam):
        self.uname = uname
        self.utype = utype
        self.sparam = sparam
        self.nparam = nparam
        self.uid = 0

    def __repr__(self):
        return "<YYUser(uname='%s'')>" % self.uname
