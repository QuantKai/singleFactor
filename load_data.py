# -*- coding:utf-8 -*-
__author__ = 'kaI'
import os
import sys
my_path = os.getcwd()
sys.path.append('D:\\kai')
from tool_kai import *
kai = ToolKai()
os.chdir(my_path)
from WindPy import *
import pandas as pd
import datetime


class LoadWindData(object):
    def __init__(self, start_date, end_date, period):
        """先定义下载日期，再定义获取数据类型，保存路径"""
        self.start_date = start_date
        self.end_date = end_date
        self.period = period

        # 保存路径
        self.trade_date_data_path = 'trade_date_data'
        self.financial_report_data_path = 'financial_report_data'

        # 主要控制函数
        self.main_download_data()

    def main_download_data(self):
        self.load_trade_date_data()
        self.load_financial_report_data()

    def load_financial_report_data(self):
        if not os.path.exists(self.financial_report_data_path):
            os.mkdir(self.financial_report_data_path)
        days = len(kai.tdays_df.loc[self.start_date:self.end_date])
        for date in kai.get_front_financial_date(trade_date=self.end_date, num=days/90+1+2):
            if not os.path.exists(os.path.join(self.financial_report_data_path, date+'.xls')):
                date_data_df = self.get_wind_data(date, 'financial_report')
                date_data_df.to_excel(os.path.join(self.financial_report_data_path, date+'.xls'))
            else:
                print date, u'financial_report数据已存在'

    def load_trade_date_data(self):
        if not os.path.exists(self.trade_date_data_path):
            os.mkdir(self.trade_date_data_path)
        tdays_df = kai.tdays_df[kai.tdays_df['tradedays_'+self.period] == 1].loc[self.start_date:self.end_date]
        for date in tdays_df.index.tolist():
            if date == datetime.datetime.now().strftime('%Y-%m-%d'):
                continue
            if not os.path.exists(os.path.join(self.trade_date_data_path, date+'.xls')):
                day_data_df = self.get_wind_data(date, 'trade_date')
                day_data_df.to_excel(os.path.join(self.trade_date_data_path, date+'.xls'))
            else:
                print date, u'trade_date数据已存在'

    def get_wind_data(self, date, style):
        print date
        w.start()
        new_df = pd.DataFrame(index=kai.all_a_stock)
        if style == 'trade_date':
            wind_data = w.wss(kai.all_a_stock,
                              "val_pe_deducted_ttm,pb_lf,ps_ttm,dividendyield2,mkt_cap_ard,mkt_cap_float,close",
                              "tradeDate="+date+";unit=1;currencyType=;priceAdj=U;cycle=D")
        elif style == 'financial_report':
            wind_data = w.wss(kai.all_a_stock, "qfa_oper_rev,qfa_net_profit_is,wgsd_qfa_deductedprofit,"
                                               "roe_avg,roa,grossprofitmargin,netprofitmargin,assetsturn,"
                                               "debttoassets,current,ocftoassets",
                              "unit=1;rptDate="+date+";rptType=1;currencyType=")
        elif style == 'technical_data':
            wind_data = w
        else:
            print u'未能识别wind类型'
            return None
        print wind_data
        for col, data in zip(wind_data.Fields, wind_data.Data):
            new_df[col] = data
        print u'获取数据:'+date, u'类型为:'+style
        return new_df
