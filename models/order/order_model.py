#coding=utf-8

from libs.db.dbsession import Base, dbSession
from sqlalchemy import Column, Integer, String, Float, Numeric
from enum import Enum


class DMOrder(Base):
    __tablename__ = 'dm_orders'

    # the unique id
    oid = Column(Integer, primary_key=True)
    pid = Column(Integer)
    olabel = Column(String(255))
    oname = Column(String(255))
    ts_code = Column(String(32))
    odirect = Column(Integer)
    amount = Column(Float)
    price = Column(Float)
    ctime = Column(String(32))
    ostatus = Column(Integer)
    dealamount = Column(Float)
    dealprice = Column(Float)
    dealtime = Column(String(32))
    nownum = Column(Float)
    costprice = Column(Float)
    lastnum = Column(Float)
    lastcost = Column(Float)
    testid = Column(Integer)
    sparam = Column(String(255))
    nparam = Column(Integer)

    def __init__(self, pid, olabel, oname, ts_code, odirect, amount, price, ctime, ostatus, dealamount, dealprice, dealtime, nownum, costprice, lastnum, lastcost, testid, sparam='', nparam=0):
        self.pid = pid
        self.olabel = olabel
        self.oname = oname
        self.ts_code = ts_code
        self.odirect = odirect
        self.amount = amount
        self.price = price
        self.ctime = ctime
        self.ostatus = ostatus
        self.dealamount = dealamount
        self.dealprice = dealprice
        self.dealtime = dealtime
        self.nownum = nownum
        self.costprice = costprice
        self.lastnum = lastnum
        self.lastcost = lastcost
        self.testid = testid
        self.sparam = sparam
        self.nparam = nparam

    def __repr__(self):
        return "<DMOrder(olabel='%s',ts_code='%s',holdvalue='%f')>" % (self.oname, self.ts_code, self.holdvalue)

