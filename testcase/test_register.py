# coding=utf-8
# author= 'Jack'
# time：2022/2/17
import allure
import pytest
import yaml
from api.baseapi import BaseApi

@allure.epic("注册")
class TestRegister(BaseApi):
    @allure.story("注册测试用例")
    @allure.title("注册测试用例")
    @allure.severity("critical")
    # @pytest.mark.parametrize("data",yaml.safe_load(open("../data/data_list.yaml",'r',encoding='utf-8'))['co_list'])
    def test_register(self):
        api=BaseApi()
        print( api.cfg_list )
        print( api.cfg_sql_ini )
        print( api.cfg_test_ini )
        # res = api.register()
        # print(res)
