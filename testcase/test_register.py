# coding=utf-8
# author= 'Jack'
# time：2022/2/17
import yaml

from api.baseapi import BaseApi


class TestRegister(BaseApi):
    def test_register(self):
        data=yaml.safe_load(open("./data/register.yaml"))
        register = TestRegister.register()
