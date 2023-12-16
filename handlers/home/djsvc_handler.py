# coding=utf-8
import uuid
import json
import datetime
import time
import math

from dateutil import rrule

import pandas as pd
import numpy as np
import talib as ta
import stockstats

from talib import MA_Type
from talib import abstract
from talib.abstract import *

from libs.db.dbsession import pro, ts
from sqlalchemy.sql import and_, or_

from threading import Thread, current_thread

import tornado.web
import tornado.websocket
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import asyncio
import nest_asyncio

from handlers.base.base_handler import BaseHandler
import matplotlib.pyplot as plt
import random

import pandas as pd
# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import pymysql
import tushare as ts
import easyquotation

import numpy as np
import matplotlib.pyplot as plt


from libs.db.dbsession import engine, tcal
from libs.db.dbsession import dbSession
from sqlalchemy import Column, Integer, String, Float, Numeric

from models.order.order_model import DMOrder

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

class AddOrderHandler(BaseHandler):
    def get(self, order_name, order_code, direciton, oprice, onum, odate):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        today = time.strftime("%Y-%m-%d",time.localtime(time.time()))

        uid = self.get_secure_cookie("uid")

        # 如果是要卖出，检测是否有足够的持仓量
        if direciton == 3:
            pass

            # 查询是否已经选入备选池
            holds = dbSession.query(DMOrder).filter(DMOrder.ts_code == order_code).all()

            total_left = 0
            for hold in holds:
                if hold.odirect == 0:
                    total_left = total_left + hold.dealnum
                elif hold.odirect == 3:
                    if total_left > hold.onum:
                        total_left = total_left - hold.dealnum
                    else:
                        total_left = 0

            if total_left < onum:
                # 已经存在，则忽略本次选择
                sReturn = {"errcode": -1, "errmsg": "没有足够的持仓可供卖出！"}
                self.write(sReturn)
                self.finish()
                return

        sitem = DMOrder(0, '', order_name, order_code, direciton, onum, oprice, odate, 2, onum, oprice, odate, onum, oprice, onum, oprice, 0)

        dbSession.add(sitem)
        dbSession.commit()
        dbSession.close()

        sReturn = {"errcode": 0, "errmsg": "新增订单成功"}
        self.write(sReturn)
        self.finish()

class FetchInfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        tss = time.time()

        sqlcmd = "select ts_code, oname, odirect, dealamount, price, dealtime from dm_orders order by dealtime"
        orders = pd.read_sql(sql=sqlcmd, con=engine)
        start_date = orders['dealtime'].iloc[0].to_pydatetime()
        end_date = datetime.datetime.now()# orders['dealtime'].iloc[-1].to_pydatetime()
        s_date = start_date.strftime("%Y%m%d")
        e_date = end_date.strftime("%Y%m%d")

        orders['cdate'] = orders['dealtime'].apply(lambda x: x.strftime("%Y%m%d"))
        orders['ttime'] = orders['dealtime'].apply(lambda x: x.strftime("%Y%m%d %H:%M:%S"))
        order_hd = orders[['ttime', 'cdate']]


        histdays = tcal[(tcal['cal_date'] <= e_date) & (tcal['cal_date'] >= s_date) & (tcal['is_open'] == 1)]

        shd = pd.DataFrame()
        ehd = pd.DataFrame()
        shd['cdate'] = [item for item in histdays['cal_date']]
        shd['ttime'] = [item + ' 00:00:00' for item in histdays['cal_date']]
        ehd['cdate'] = [item for item in histdays['cal_date']]
        ehd['ttime'] = [item + ' 23:59:59' for item in histdays['cal_date']]

        new_hd = shd.append(ehd)
        last_hd = new_hd.append(order_hd).sort_values(by='ttime').reset_index(drop=True)
        last_hd['cvalue'] = 0.0
        print("Process 111111111111 =", time.time() - tss)

        hold_list = pd.DataFrame(columns=["ts_code", "lvalue"])

        item_lists = []
        stock_lists = orders.ts_code.unique()
        for stock_code in stock_lists:  # [:23]:
            print('Process stock:' + stock_code)
            print("Process 333333333333333333 =", time.time() - tss)
            kline = pro.daily(ts_code=stock_code, start_date=s_date, end_date=e_date)
            kline = kline[::-1]

            m_kline = pd.DataFrame()
            m_kline['cdate'] = [item for item in kline['trade_date']]
            m_kline['ttime'] = [item + ' 00:00:00' for item in kline['trade_date']]
            m_kline['price'] = [item for item in kline['open']]

            c_kline = pd.DataFrame()
            c_kline['cdate'] = [item for item in kline['trade_date']]
            c_kline['ttime'] = [item + ' 23:59:59' for item in kline['trade_date']]
            c_kline['price'] = [item for item in kline['close']]

            o_kline = m_kline.append(c_kline).sort_values(by='ttime').reset_index(drop=True)
            item_hd = pd.merge(last_hd, o_kline, on=['cdate', 'ttime'], how='left')

            item_orders = orders.loc[orders['ts_code'] == stock_code]
            item_kline = pd.merge(o_kline, item_orders, on=['ttime', 'cdate', 'price'], how='outer').fillna(0)
            item_kline = item_kline.fillna(0)

            item_list = pd.merge(last_hd, item_kline, on=['ttime', 'cdate'], how='outer').fillna(0)
            item_list['price'].replace(0, np.nan, inplace=True)
            item_list[::-1].bfill(inplace=True)
            item_list['price'].fillna(0, inplace=True)
            # print(item_list['price'])

            item_list['kdirect'] = -2 * item_list['odirect'] / 3 + 1
            # print(item_list['kdirect'].tolist())
            item_list['holdnum'] = 0
            item_list['fee'] = 0.0
            last_hn = 0
            for ix, row in item_list.iterrows():
                if ix == 0:
                    continue

                # if row.price == 0.0:
                #   item_list.loc[item_list['ttime'] == row['ttime'], 'price'] = item_list.iloc[ix-1]

                # last_hn = item_list.iloc[ix-1]['holdnum']
                hn = row['kdirect'] * row['dealamount']
                if hn > 0:
                    hn = last_hn + hn
                    last_hn = hn
                if hn == 0:
                    hn = last_hn
                if hn < 0:
                    hn = last_hn + hn
                    if hn < 0:
                        hn = 0
                    last_hn = hn
                if hn > 0:
                    item_list.loc[item_list['ttime'] == row['ttime'], 'holdnum'] = hn
                    # print(hn, row['holdnum'], item_list.iloc[ix]['holdnum'])

                # 计算手续费
                if row.kdirect == -1:
                    fee = 0.0 - row.dealamount * row.price * 0.001
                    item_list.loc[item_list['ttime'] == row['ttime'], 'fee'] = fee

                valuechange = (item_list.iloc[ix].price - item_list.iloc[ix - 1].price) * item_list.iloc[
                    ix - 1].holdnum * 1.0 + item_list.iloc[ix].fee + item_list.iloc[ix - 1].cvalue
                item_list.loc[item_list['ttime'] == row['ttime'], 'cvalue'] = valuechange
            # item_list['cvalue'] = (item_list.price - item_list.price.shift(1)) * item_list.holdnum * 100.0 + item_list.cvalue.shift(1) + item_list.fee

            # print(stock_code, item_list[['ttime', 'price', 'holdnum', 'cvalue']])
            # print(item_list['price'].tolist())
            # print(item_list['holdnum'].tolist())
            # print(item_list['fee'].tolist())
            # print(item_list['cvalue'].tolist())
            item_lists.append(item_list)

            last_hold = item_list['holdnum'].iloc[-1]
            if last_hold > 0:
                lvalue = last_hold * item_list['price'].iloc[-1]
                hold_list = hold_list.append({"ts_code": stock_code, "lvalue": lvalue}, ignore_index=True)
        print("Process 4444444444444444 =", time.time() - tss)

        calc_date_diff = rrule.rrule(freq=rrule.DAILY, dtstart=start_date, until=end_date)
        print(hold_list)

        last_hd['cvalue'] = 0000.0
        for item in item_lists:
            last_hd['cvalue'] += item['cvalue']

        print(last_hd['cdate'].tolist())
        print(last_hd['cvalue'].tolist())
        print("Process 55555555555555555 =", time.time() - tss)

        #plt.figure()
        #plt.plot(last_hd['cdate'].values, last_hd['cvalue'].values)
        #plt.show()

        # 9元买入10000股花费9万，升到12元，赚3元一股，合计赚30000元
        # 9元买入100股，花费900，赚300
        # 3*100

        last_equity = last_hd['cvalue'].iloc[-1]
        today_profit = last_hd['cvalue'].iloc[-1] - last_hd['cvalue'].iloc[-2]
        stock_nums = len(hold_list)
        annual_pv = (last_hd['cvalue'].iloc[-1] - last_hd['cvalue'].iloc[0]) * calc_date_diff.count() * 100.0 / 365 / 300000.0
        stockjsons = []
        for ix, hold in hold_list.iterrows():
            stockjsons.append({"name": hold['ts_code'], "value": hold['lvalue']})

        seljsons = last_hd.to_json(orient="records", force_ascii=False)
        retdatas = {"errcode": 0, "errmsg": "查询信息成功", "last_equity": last_equity, "stock_nums": stock_nums, "today_profit": today_profit, "annual_pv": annual_pv, "stock_list": stockjsons, "valuelist": seljsons}

        self.write(retdatas)
        self.finish()

class FetchOrderListHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        sqlcmd = 'select p.* from dm_orders p order by p.dealtime desc'
        pools = pd.read_sql(sql=sqlcmd, con=engine)

        seljsons = pools.to_json(orient="records", force_ascii=False)
        self.write(seljsons)
        self.finish()
