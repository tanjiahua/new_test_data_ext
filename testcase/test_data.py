# coding=utf-8
# author= 'Jack'
# time：2022/3/5
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import allure
import pytest
import yaml
from common.params_init import loan_data


@allure.epic("测试获取的数据初始化")
class Test_Data():
    @allure.story("数据初始化操作")
    @allure.title("数据初始化操作")
    @allure.severity("critical")
    @pytest.mark.parametrize("list_data",yaml.safe_load(open("./data/pk_list_data.yaml","r",encoding="UTF-8")))
    def test_data(self,list_data):
        with allure.step("执行测试操作"):
            data = loan_data(list_data[0],list_data[1],list_data[2],list_data[3])
            param=data.return_data()
            print(param)


