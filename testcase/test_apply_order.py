# coding=utf-8
# author= 'Jack'
# time：2021/9/7
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import allure
import pytest
import yaml
from api.baseapi import BaseApi


@allure.epic("订单流程测试")

class Test_Apply_Order():
    @allure.story("借款订单流程测试")
    @allure.title("借款订单流程测试")
    @allure.severity("critical")
    @pytest.mark.parametrize("list_data",yaml.safe_load(open("./data/pk_list_data.yaml","r",encoding="UTF-8")))
    def test_apply_order(self,list_data):
        with allure.step("注册，登录，填写个人信息，申请借款"):
            run_test = BaseApi(list_data[0], list_data[1], list_data[2], list_data[3])
            run_test.main_run(order_count=1)  # 新用户进件放款
