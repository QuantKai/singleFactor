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


class TechnicalFactor(object):
    def __init__(self, date, period):
        pass


print kai.tdays_df[kai.tdays_df['tradedays_w']==1].index.tolist()
