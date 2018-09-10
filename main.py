# -*- coding:utf-8 -*-
__author__ = 'kaI'
from single_factor import *

if __name__ == '__main__':
    single_factory = SingleFactor(start_date='2018-08-20', end_date=datetime.datetime.now().strftime('%Y-%m-%d'),
                                  period='w')
