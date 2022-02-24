# coding=utf-8
# author= 'Jack'
# time：2022/1/6
import json
import os
import time

import requests
from common import logging_func
log = logging_func.Logger().logger
path = os.path.dirname(os.path.abspath(__file__))

class  H5apply():

    def __init__(self):
        self.headers = {'Content-Type': 'application/json;charset=utf-8',
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Infinix X657B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36'}
        self.host="http://172.20.240.143:8012"

    def checkUserExist(self,mobile):
        url=self.host + "/app/api/multi/v2/checkUserExist"
        headers=self.headers
        data={"userSource":"2","appId":"AL158","channelCode":"aceloan","mobile":mobile}
        data=json.dumps(data)
        res=requests.post(url, headers=headers, data=data)
        if "Successful" in res.text:
            log.info( "检查手机号成功" )
        else:
            log.info( "检查手机号失败" )

    def sendSmsCode(self,mobile):
        url=self.host + "/app/api/multi/v2/sendSmsCode"
        headers=self.headers
        data={"userSource":"2","appId":"AL158","channelCode":"aceloan","language":"en_US","loginType":"0","mobile":mobile,"smsCodeType":"REGISTER"}
        data=json.dumps(data)
        res = requests.post( url, headers=headers, data=data )
        if "Successful" in res.text:
            log.info( "发送验证码成功" )
        else:
            log.info( "发送验证码失败" )

    def userRegister(self,mobile):
        url=self.host + "/app/api/multi/v2/userRegister"
        headers=self.headers
        data={"userSource":"2","appId":"AL158","channelCode":"aceloan","mobile":mobile,"smsCode":"123456","optMode":1,"registerSource":"facebook","clientType":"WEB","password":"poiu0qwer509495"}
        data=json.dumps(data)
        res = requests.post( url, headers=headers, data=data )
        if "Successful" in res.text:
            log.info( "注册成功" )
        else:
            log.info( "注册失败" )
    def login(self,mobile):
        url=self.host + "/app/api/multi/v2/login"
        headers=self.headers
        data={"userSource":"2","appId":"AL158","channelCode":"aceloan","mobile":mobile,"smsCode":"123456","optMode":1,"registerSource":"H5","clientType":"WEB","smsCodeType":"LOGIN","deviceInfoId":"C38D63C3B1C3AC","password":"D5Y3fd6Rz7ZFdEidxAjqfA=="}
        data=json.dumps(data)
        res = requests.post( url, headers=headers, data=data )
        if "Successful" in res.text:
            log.info( "登录成功" )
        else:
            log.info( "登录失败" )
        self.token=res.json()['data']['token']

    def fillInUserInfo(self):
        url=self.host + "/app/api/multi/v2/user/fillInUserInfo"
        headers=self.headers
        headers['Authorization']=self.token
        data= \
            {"userSource": "2", "appId": "AL158", "channelCode": "aceloan", "firstName": "Jimik", "middleName": "Tol",
             "lastName": "Ander", "birthday": "1990-01-01", "marryStatus": "1", "sex": "0", "email": "ander@gmail.com",
             "whatsApp": "01639100154"}
        data=json.dumps(data)
        res = requests.post( url, headers=headers, data=data )
        if "Successful" in res.text:
            log.info( "提交个人信息成功" )
        else:
            log.info( "提交个人信息失败" )

    def saveContacts(self):
        url=self.host + "/app/api/multi/v2/saveContacts"
        headers=self.headers
        headers['Authorization']=self.token
        data= \
            {"userSource":"2","appId":"AL158","channelCode":"aceloan","contacts":[{"relation":"PARENT","name":"David","mobile":"04343484494"},{"relation":"SPOUSE","name":"Alan","mobile":"04334545548"},{"relation":"FRIEND","name":"Billy","mobile":"01334876765"}]}
        data=json.dumps(data)
        res = requests.post( url, headers=headers, data=data )
        if "Successful" in res.text:
            log.info( "提交紧急联系人信息成功" )
        else:
            log.info( "提交紧急联系人信息失败" )

    def run_main(self,mobile):
        self.checkUserExist(mobile)
        self.sendSmsCode(mobile)
        self.userRegister(mobile)
        self.login(mobile)
        self.fillInUserInfo()
        self.saveContacts()



if __name__ == '__main__':
    mobile = '0' + str(int(time.time()))
    log.info("H5进件的手机号: "+" "+  mobile)
    H5apply=H5apply()
    H5apply.run_main(mobile)