# coding=utf-8
# author= 'Jack'
# time：2022/2/16
import pytest
import yaml

class TestYaml():
    @pytest.mark.parametrize("data",yaml.safe_load(open("./loan_list.yaml")))
    def testyaml(self,data):
        print(data)

    def testyaml2(self):
        slogan = [['co', 'test_ini_co.ini', 'sql_ini_co.ini', 'monni'],
            ['co', 'test_ini_co.ini', 'sql_ini_co.ini', 'prestamodinero'],
            ['co', 'test_ini_co.ini', 'sql_ini_co.ini', 'pcamion']]
        website = {'url': 'www.12345678'}

        print( slogan )
        print( website )

        print( yaml.dump( slogan ) )
        print( yaml.dump( website ) )