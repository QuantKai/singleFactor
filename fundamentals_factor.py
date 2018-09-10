# -*- coding:utf-8 -*-
__author__ = 'kaI'
import os
import sys
my_path = os.getcwd()
sys.path.append('D:\\kai')
from tool_kai import *
kai = ToolKai()
os.chdir(my_path)
import pandas as pd
import numpy as np
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


class CalculateFundamentalsFactor(object):
    def __init__(self, date, period):
        self.date = date
        self.period = period
        self.df = pd.DataFrame(index=kai.all_a_stock)
        self.trade_date_data_path = 'trade_date_data'
        self.financial_report_data_path = 'financial_report_data'
        self.financial_date_list, self.financial_data_dict, self.trade_date_list, self.trade_data_dict \
            = self.data_preparation()
        
        # 主要控制函数
        self.main_get_fundamentals_factor()

    def data_preparation(self):
        """通用型数据准备, 存放于dict中"""
        financial_date_list = kai.get_front_financial_date(self.date, num=2, ahead=0)
        financial_date_list.sort(reverse=True)
        financial_data_dict = {}
        trade_date_list = kai.get_front_trade_date(self.date, num=2, period=self.period, ahead=0)
        trade_date_list.sort(reverse=True)
        if trade_date_list[0] == datetime.datetime.now().strftime('%Y-%m-%d'):
            del trade_date_list[0]
        trade_data_dict = {}
        # 交易日数据
        for date in financial_date_list:
            financial_data_dict[date] = pd.read_excel(os.path.join(self.financial_report_data_path, date+'.xls'),
                                                      index_col=0)
        for date in trade_date_list:
            trade_data_dict[date] = pd.read_excel(os.path.join(self.trade_date_data_path, date+'.xls'),
                                                  index_col=0)
        return financial_date_list, financial_data_dict, trade_date_list, trade_data_dict

    def main_get_fundamentals_factor(self):
        """运行因子计算"""
        # 估值类
        self.pe_ttm()
        self.pb_ttm()
        self.ps_ttm()
        self.dividend_yield()
        # 成长类
        self.oper_rev_chg()
        self.net_profit_chg()
        self.deducted_profit_chg()
        self.roe_chg()
        # 质量类
        self.roe()
        self.roa()
        self.grossprofitmargin()
        self.net_profit_margin()
        # 财务质量
        self.assets_turn()
        self.debt_to_assets()
        self.current()
        self.ocf_to_assets()
        # 规模类
        self.mkt_cap()
        self.mkt_cap_float()
        self.price()

        # 非常规因子
        self.peg()
        self.peg_ope()

    # 常规因子定义-------------------------------------------------------------------------------------------------

    def pe_ttm(self):
        """扣非市盈率倒数，排序1"""
        self.df['ep_ttm'] = 1/self.trade_data_dict[self.trade_date_list[0]]['VAL_PE_DEDUCTED_TTM']

    def pb_ttm(self):
        """市净率倒数, 排序1"""
        self.df['pb_lf'] = 1/self.trade_data_dict[self.trade_date_list[0]]['PB_LF']

    def ps_ttm(self):
        """市销率倒数, 排序1"""
        self.df['ps_ttm'] = 1/self.trade_data_dict[self.trade_date_list[0]]['PS_TTM']

    def dividend_yield(self):
        """股息率, 排序1"""
        self.df['dividend_yield'] = self.trade_data_dict[self.trade_date_list[0]]['DIVIDENDYIELD2']

    def oper_rev_chg(self):
        """营业收入增长率, 排序1"""
        self.df['oper_rev_chg'] = ((self.financial_data_dict[self.financial_date_list[0]]['QFA_OPER_REV']
                                    - self.financial_data_dict[self.financial_date_list[1]]['QFA_OPER_REV']) /
                                   self.financial_data_dict[self.financial_date_list[1]]['QFA_OPER_REV'])

    def net_profit_chg(self):
        """净利润增长率, 排序1"""
        self.df['net_profit_chg'] = ((self.financial_data_dict[self.financial_date_list[0]]['QFA_NET_PROFIT_IS']
                                      - self.financial_data_dict[self.financial_date_list[1]]['QFA_NET_PROFIT_IS']) /
                                     self.financial_data_dict[self.financial_date_list[1]]['QFA_NET_PROFIT_IS'])

    def deducted_profit_chg(self):
        """扣除非经常性损益利润增长率, 排序1"""
        self.df['deducted_profit_chg'] = ((self.financial_data_dict[self.financial_date_list[0]]['WGSD_QFA_DEDUCTEDPROFIT']
                                           - self.financial_data_dict[self.financial_date_list[1]]['WGSD_QFA_DEDUCTEDPROFIT']) /
                                          self.financial_data_dict[self.financial_date_list[1]]['WGSD_QFA_DEDUCTEDPROFIT'])

    def roe_chg(self):
        """roe增长率, 排序1"""
        self.df['roe_chg'] = ((self.financial_data_dict[self.financial_date_list[0]]['ROE_AVG']
                               - self.financial_data_dict[self.financial_date_list[1]]['ROE_AVG']) /
                              self.financial_data_dict[self.financial_date_list[1]]['ROE_AVG'])

    def roe(self):
        """roe, 排序1"""
        self.df['roe'] = self.financial_data_dict[self.financial_date_list[0]]['ROE_AVG']

    def roa(self):
        """roe, 排序1"""
        self.df['roa'] = self.financial_data_dict[self.financial_date_list[0]]['ROA']

    def grossprofitmargin(self):
        """毛利率, 排序1"""
        self.df['grossprofitmargin'] = self.financial_data_dict[self.financial_date_list[0]]['GROSSPROFITMARGIN']

    def net_profit_margin(self):
        """销售净利率, 排序1"""
        self.df['net_profit_margin'] = self.financial_data_dict[self.financial_date_list[0]]['NETPROFITMARGIN']

    def assets_turn(self):
        """总资产周转率, 排序1"""
        self.df['assets_turn'] = self.financial_data_dict[self.financial_date_list[0]]['ASSETSTURN']

    def debt_to_assets(self):
        """资产负债率, 排序1"""
        self.df['debt_to_assets'] = 1/(self.financial_data_dict[self.financial_date_list[0]]['DEBTTOASSETS'])

    def current(self):
        """流动比率, 排序1"""
        self.df['current'] = self.financial_data_dict[self.financial_date_list[0]]['CURRENT']

    def ocf_to_assets(self):
        """资产的现金流量回报率, 排序1"""
        self.df['ocf_to_assets'] = self.financial_data_dict[self.financial_date_list[0]]['OCFTOASSETS']

    def mkt_cap(self):
        """总市值, 排序1"""
        self.df['mkt_cap'] = 1/np.log(self.trade_data_dict[self.trade_date_list[0]]['MKT_CAP_ARD'])

    def mkt_cap_float(self):
        """流通市值, 排序1"""
        self.df['mkt_cap_float'] = 1/np.log(self.trade_data_dict[self.trade_date_list[0]]['MKT_CAP_FLOAT'])

    def price(self):
        """价格，排序1"""
        self.df['price'] = 1/np.abs(np.log(self.trade_data_dict[self.trade_date_list[0]]['CLOSE']))

    # 非常规因子定义-------------------------------------------------------------------------------------------------

    def peg(self):
        """PEG_扣非净利润, 排序1"""
        def remark(x):
            if x < 0:
                return 0.0000001
            else:
                return x

        g = self.financial_data_dict[self.financial_date_list[0]]['QFA_NET_PROFIT_IS'] /\
            self.financial_data_dict[self.financial_date_list[1]]['QFA_NET_PROFIT_IS']
        g = g.apply(lambda x: remark(x))
        self.df['peg'] = g/self.trade_data_dict[self.trade_date_list[0]]['VAL_PE_DEDUCTED_TTM']

    def peg_ope(self):
        def remark(x):
            if x < 0:
                return 0.0000001
            else:
                return x

        g = self.financial_data_dict[self.financial_date_list[0]]['QFA_OPER_REV'] /\
            self.financial_data_dict[self.financial_date_list[1]]['QFA_OPER_REV']
        g = g.apply(lambda x: remark(x))
        self.df['peg_ope'] = g/self.trade_data_dict[self.trade_date_list[0]]['VAL_PE_DEDUCTED_TTM']
