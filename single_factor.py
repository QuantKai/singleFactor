# -*- coding:utf-8 -*-
__author__ = 'kaI'
import os
import sys
my_path = os.getcwd()
sys.path.append('D:\\kai')
from tool_kai import *
kai = ToolKai()
os.chdir(my_path)
import datetime
import pandas as pd
import numpy as np
import load_data
import fundamentals_factor

reload(sys)
sys.setdefaultencoding('utf-8')


class SingleFactor(object):
    def __init__(self, start_date='2018-08-20', end_date=datetime.datetime.now().strftime('%Y-%m-%d'), period='w'):
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.factor_path = 'factor_data'
        self.hold_path = 'hold'
        # 下载数据
        load_data.LoadWindData(start_date=self.start_date, end_date=self.end_date, period=self.period)
        # 计算因子数据
        self.main_get_factor()

    def main_get_factor(self):
        if not os.path.exists(self.factor_path):
            os.mkdir(self.factor_path)
        if not os.path.exists(self.hold_path):
            os.mkdir(self.hold_path)
        tdays_df = kai.tdays_df[kai.tdays_df['tradedays_'+self.period] == 1].loc[self.start_date:self.end_date]
        for date in tdays_df.index.tolist():
            if not os.path.exists(os.path.join(self.factor_path, date+'.xls')):
                df = fundamentals_factor.CalculateFundamentalsFactor(date, self.period).df
                df.to_excel(os.path.join(self.factor_path, date+'.xls'))
            else:
                print date, u'factor数据已存在'
                df = pd.read_excel(os.path.join(self.factor_path, date+'.xls'), index_col=0)
            df = self.industry_normalization(df)
            self.get_stocks(df, date, 200)

    def get_stocks(self, factor_df, date, stocks_num):
        save_path = os.path.join(os.path.join(self.hold_path, date))
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        factor_df = kai.drop_st(factor_df)
        factor_df = kai.drop_new(factor_df)
        # factor_df = kai.drop_suspend(factor_df, factor_file.decode('gbk').split('.')[0])
        for col in factor_df:
            factor_df = factor_df.sort_values(by=[col], ascending=False)
            save_df = pd.DataFrame(index=factor_df[0:stocks_num].index)
            save_df = pd.merge(save_df, kai.all_a_stock_df, left_index=True, right_index=True, how='left')
            save_df = save_df.drop(['SHSC', 'SHSC2', 'marginornot', 'ipo_date'], axis=1)
            save_df['weight'] = 100.00000/len(save_df)
            save_df.index.name = 'stock'
            save_df.to_excel(os.path.join(save_path, '1'+col+'.xls'))

    def industry_normalization(self, factor_df):
        # 行业因子高斯正则化
        def normalization(data_list):
            """# 行业精选model"""
            average = np.average(data_list)
            std = np.std(data_list)
            return [(x-average)/std for x in data_list]
        factor_df = pd.merge(factor_df, kai.all_a_stock_df, left_index=True, right_index=True, how='left')
        factor_df = factor_df.drop(['SHSC', 'SHSC2', 'marginornot', 'ipo_date', 'sec_name'], axis=1)
        factor_df = factor_df.fillna(0)
        factor_group_list = list(factor_df.groupby(['industry']))
        save_df = pd.DataFrame()
        for group in factor_group_list:
            for col in group[1]:
                if col == 'industry':
                    continue
                group[1][col] = normalization(group[1][col])
            if group[0] == 0:
                continue
            save_df = save_df.append(group[1])
        save_df = save_df.drop(['industry'], axis=1)
        return save_df
