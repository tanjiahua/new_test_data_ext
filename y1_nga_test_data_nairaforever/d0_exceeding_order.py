# !/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Date      :2021/12/19
# FileName  :d0_exceeding_order.py
# Describe  :
# Author    :liwenli


import os
import sys


path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(sys.path[0]))
from new_apply_order import NewUserApplyOrder
cfg_alick = ['nga', 'test_ini_nga.ini', 'sql_ini_nga.ini', 'nairaforever']
os.environ['cfg_alick'] = str(cfg_alick)
cs2 = NewUserApplyOrder(*cfg_alick)
cs2.main_run()  # 新用户进件放款
cs2.allow_extension(days_modify=-1)  # 临期订单展期