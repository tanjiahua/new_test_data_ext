# !/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Date      :2021/12/19
# FileName  :order_status_40.py
# Describe  :
# Author    :liwenli
import os
import sys


path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(sys.path[0]))
from new_apply_order import NewUserApplyOrder

cfg_alick = ['nga', 'test_ini_nga.ini', 'sql_ini_nga.ini', 'moneyaccess']
os.environ['cfg_alick'] = str(cfg_alick)
cs2 = NewUserApplyOrder(*cfg_alick)
cs2.main_run(order_count=1)  # 新用户进件放款
cs2.syn_dun_order(days_modify=-1)  # 临期同步催收