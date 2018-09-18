# -*- coding:utf-8 -*-
__author__ = 'kaI'
import os
import sys
my_path = os.getcwd()
sys.path.append('D:\\kai')
from tool_kai import *
kai = ToolKai(back_test_data=True, back_test_update=False)
os.chdir(my_path)
import datetime
import pandas as pd
import numpy as np


class TechnicalFactor(object):
    def __init__(self, date, period):
        self.date = date
        self.df = pd.DataFrame(index=kai.all_a_stock)
        self.technical_path = 'technical_data'
        self.all_a_close_df = kai.all_a_close_df
        self.all_a_vwap_df = kai.all_a_vwap_df

        self.main_get_technical_factor()

    def main_get_technical_factor(self):
        """运行因子计算"""
        # 动量类
        self.momentum()
        # 反转类
        self.reverse_p()

        # 自定义动量因子
        self.momentum_chg2()

    def momentum(self):
        momentum_list = [5, 10, 20]
        for mom in momentum_list:
            date_list = kai.get_front_trade_date(trade_date=self.date, period='d', num=mom+1, ahead=0)
            print date_list[0], date_list[-1]
            self.df['momentum_'+str(mom)] = ((self.all_a_close_df[date_list[0]] - self.all_a_close_df[date_list[-1]]) /
                                             self.all_a_close_df[date_list[-1]])*100

    def reverse_p(self):
        reverse_list = [5, 10, 20]
        for rev in reverse_list:
            date_list = kai.get_front_trade_date(trade_date=self.date, period='d', num=rev+1, ahead=0)
            self.df['reverse_'+str(rev)] = ((self.all_a_close_df[date_list[0]] - self.all_a_close_df[date_list[-1]]) /
                                            self.all_a_close_df[date_list[-1]])*-100

    def volatility(self):
        pass

    def momentum_chg(self):
        all_a_vwap_df = self.all_a_vwap_df
        all_a_vwap_df = all_a_vwap_df.replace(0.00, np.nan)
        momentum_date = 5
        chg_limit = 0.03
        new_df = pd.DataFrame(index=kai.all_a_stock)
        date_list = kai.get_front_trade_date(trade_date=self.date, period='d', num=momentum_date+1, ahead=0)
        new_df['sum'] = 0
        for date in date_list:
            new_df[date] = all_a_vwap_df[date]
            new_df['sum'] += all_a_vwap_df[date]
        new_df['close'] = (all_a_vwap_df[date_list[0]]-new_df['sum']/len(date_list))/new_df['sum']*len(date_list)
        new_df['tendency'] = (all_a_vwap_df[date_list[0]]+all_a_vwap_df[date_list[1]]) / \
                             (all_a_vwap_df[date_list[-1]]+all_a_vwap_df[date_list[-2]])
        new_df['tendency'] = new_df['tendency']*new_df['close']
        new_df['chg'] = (all_a_vwap_df[date_list[0]]-all_a_vwap_df[date_list[-1]])/all_a_vwap_df[date_list[-1]]
        new_df['chg'] = new_df['chg'].map(lambda x: x if x > 0 else 0)
        new_df['chg'] = new_df['chg'].map(lambda x: x if x < chg_limit else 0)
        new_df['result'] = new_df['chg']*new_df['tendency']
        self.df['momentum_chg'] = new_df['result']

    def momentum_chg2(self):
        all_a_vwap_df = self.all_a_vwap_df
        all_a_vwap_df = all_a_vwap_df.replace(0.00, np.nan)
        momentum_date = 5
        chg_limit = 0.03
        new_df = pd.DataFrame(index=kai.all_a_stock)
        date_list = kai.get_front_trade_date(trade_date=self.date, period='d', num=momentum_date+1, ahead=0)
        new_df['sum'] = 0
        for date in date_list:
            new_df[date] = all_a_vwap_df[date]
            new_df['sum'] += all_a_vwap_df[date]
        new_df['close'] = (all_a_vwap_df[date_list[0]]-new_df['sum']/len(date_list))/new_df['sum']*len(date_list)
        new_df['tendency'] = (all_a_vwap_df[date_list[0]]+all_a_vwap_df[date_list[1]]) / \
                             (all_a_vwap_df[date_list[-1]]+all_a_vwap_df[date_list[-2]])
        new_df['tendency'] = new_df['tendency']*new_df['close']
        new_df['chg'] = (all_a_vwap_df[date_list[0]]-all_a_vwap_df[date_list[-1]])/all_a_vwap_df[date_list[-1]]
        new_df['chg'] = new_df['chg'].map(lambda x: x if x > 0 else 0)
        new_df['chg'] = new_df['chg'].map(lambda x: x if x < chg_limit else 0)
        new_df['result'] = new_df['chg']*new_df['tendency']
        self.df['momentum_chg'] = new_df['result']

a = TechnicalFactor('2018-09-07', 'd')
