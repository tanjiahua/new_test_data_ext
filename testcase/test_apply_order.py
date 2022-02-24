# coding=utf-8
# author= 'Jack'
# time：2021/9/7
from api.baseapi import BaseApi
from common import params_init as p

def test_apply_order():
    cfg_list=p.loan_data.cfg_list
    for cfg_alick in cfg_list:
        cs = BaseApi(*cfg_alick)
        cs.main_run(order_count=1)  # 新用户进件放款

if __name__ == '__main__':
     test_apply_order()