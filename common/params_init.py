# !/usr/local/python3
# -*- coding:utf-8 -*-
# Date      :2021/3/27
# FileName  :param_init.py
# Describe  :
# Author    :jack
import random
import string
import time
import os
from configparser import ConfigParser
from config_ini import loan_list


class loan_data(object):

    cfg_list = loan_list.nga_list

    def __init__(self, env_mark, test_ini, sql_ini, app_name):
        self.env_mark = env_mark
        self.test_ini = test_ini
        self.sql_ini = sql_ini
        self.cfg_sql_ini = self.read_ini(self.sql_ini)
        self.cfg_test_ini = self.read_ini(self.test_ini)
        self.param = 'global_param_' + app_name
        self.app_name = app_name
        self.user_id = self.cfg_test_ini.get(self.param, 'userid')
    def get_init_file(self,test_mark):
        self.test_mark=test_mark
        if self.test_mark == 'nga':
            self.test_ini_name = 'test_ini_nga.ini'
        elif self.test_mark == 'mx':
            self.test_ini_name = 'test_ini_mx.ini'
        elif test_mark == 'ke':
            self.test_ini_name = 'test_ini_ke.ini'
        elif test_mark == 'co':
            self.test_ini_name = 'test_ini_co.ini'
        elif test_mark == 'pk':
            self.test_ini_name = 'test_ini_pk.ini'
        cfg = ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__))
        cfg.read(path + '/../config_ini/%s' % self.test_ini_name)
        return cfg


    def return_data(self,mark,param):
        self.cfg_ = loan_data.get_init_file(self,mark)
        self.appid = self.cfg_.get(param, 'appid')
        self.channelcode = self.cfg_.get(param, 'channelcode')
        self.clientcode = self.cfg_.get(param, 'clientcode')
        self.appversion = self.cfg_.get(param, 'appversion')
        self.language = self.cfg_.get(param, 'language')
        self.mobile = self.cfg_.get('mobile_idcard', 'mobile')
        self.idcard = self.cfg_.get('mobile_idcard', 'idcard')
        self.url = self.cfg_.get( 'app_url', 'app_url' )
        self.admin_web_url = self.cfg_.get('admin_web', 'url')
        self.xxl_job = self.cfg_.get('admin_web', 'xxl_job')
        self.transfer_url = self.cfg_.get('admin_web', 'transfer_url')
        self.appPackageName = self.cfg_.get(param, 'appPackageName')
        self.registersource = self.cfg_.get(param, 'registersource')
        self.appname = self.cfg_.get(param, 'appname')
        self.mp4_url = self.cfg_.get(param, 'mp4_url')
        self.authorization = self.cfg_.get(param, 'authorization')
        self.userId = self.cfg_.get(param, 'userId')
        key = ['appname', 'appid', 'channelcode', 'clientcode', 'appversion',
               'language', 'mobile', 'url', 'admin_web_url', 'xxl_job',
               'transfer_url', 'appPackageName', 'registersource', 'mp4_url',
               'authorization', 'userId']
        value = [self.appname, self.appid, self.channelcode, self.clientcode, self.appversion, self.language,
                 self.mobile, self.url, self.admin_web_url, self.xxl_job, self.transfer_url, self.appPackageName,
                 self.registersource, self.mp4_url, self.authorization, self.userId]
        param = dict(zip(key, value))
        # 检测手机号是否注册
        self.headers_checkUserExist = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': '',
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }

        self.data_checkUserExist = {
            "mobile": param['mobile'],
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099306,
            "devLongitude": 113.309291,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28", "osVersion": "9",
            "version": param['appversion']}

        self.url_checkUserExist = 'http://' + param['url'] + '/app/api/multi/v2/checkUserExist/' + param['appid']

        # 发送注册短信
        self.headers_sendSmsCode = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_sendSmsCode = {"loginType": "0",
                            "mobile": param['mobile'],
                            "smsCodeType": "REGISTER",
                            "appId": param['appid'],
                            "appName": param['appname'],
                            "appPackageName": param['appid'],
                            "appVersion": param['appversion'],
                            "brand": "Xiaomi",
                            "channelCode": param['channelcode'],
                            "clientType": "ANDROID",
                            "devLatitude": 23.099306,
                            "devLongitude": 113.309291,
                            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
                            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
                            "language": param['language'],
                            "mobileType": "platina",
                            "os": "28",
                            "osVersion": "9",
                            "version": param['appversion']}
        self.url_sendSmsCode = 'http://' + param['url'] + '/app/api/multi/v2/sendSmsCode/' + param['appid']

        # 用户注册
        self.headers_userRegister = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0'
        }
        self.data_userRegister = {
            "devI": "",
            "imei": "",
            "isSkipDecrypt": True,
            "mobile": param['mobile'],
            "otpMode": "1",
            "password": "31872",  # mx
            # "password": "13416",#nga
            "referer": "",
            "registerPageType": "0",
            "registerSource": param['registersource'],
            "smsCode": "123456",
            "tdToken": "",
            "twogIp": "",
            "udid": "",
            "wifiAddr": "",
            "wifiLatitude": 0,
            "wifiLongitude": 0,
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099306,
            "devLongitude": 113.309291,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion']
        }
        self.url_userRegister = 'http://' + param['url'] + '/app/api/multi/v2/userRegister/' + param['appid']

        # 发送登录短信
        self.headers_sendloginSmsCode = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_sendloginSmsCode = {"loginType": "0",
                            "mobile": param['mobile'],
                            "smsCodeType": "LOGIN",
                            "appId": param['appid'],
                            "appName": param['appname'],
                            "appPackageName": param['appid'],
                            "appVersion": param['appversion'],
                            "brand": "Xiaomi",
                            "channelCode": param['channelcode'],
                            "clientType": "ANDROID",
                            "devLatitude": 23.099306,
                            "devLongitude": 113.309291,
                            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
                            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
                            "language": param['language'],
                            "mobileType": "platina",
                            "os": "28",
                            "osVersion": "9",
                            "version": param['appversion']}
        self.url_sendloginSmsCode = 'http://' + param['url'] + '/app/api/multi/v2/sendSmsCode/' + param['appid']

        # 用户短信验证码登录
        self.headers_smslogin = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': '',
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }

        self.data_smslogin = {
            "devIp": "",
            "imei": "",
            "mobile": param['mobile'],
            "otpMode": "1",
            "pushToken": "test push token",
            "smsCode": "123456",
            "sysVersion": "9",
            "tdToken": "",
            "udid": "",
            "wifiAddr": "",
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099306,
            "devLongitude": 113.309291,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }
        self.url_smslogin = 'http://' + param['url'] + '/app/api/multi/v2/smsLogin/' + param['appid']

        # 提交个人信息
        self.headers_fillInUserInfo = {
            'Host':  param['url'],
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'http://172.20.240.121',
            'Accept-Language': param['language'],
            'Authorization': param['authorization'],
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
            'AppVersion': param['appversion'],
            'Referer': 'http://172.20.240.121/static/native_web/%s/' % (param['appid']),
            'X-Requested-With': param['appPackageName']
        }
        namelist=['Aaron','Abe','Abelard','Abraham','Adam','Adrian','Aidan','Alva','Alex','Alexander','Alan','Eilian','Ailin','Albert','Alfred','Andrew','Andy','Angus','Anthony','Apollo','Arnold','Arthur','August','Austin','Ben','Benjamin','Bert','Benson','Bill','Billy','Blake','Bob','Bobby','Brad','Brandon','Brant','Brent','Bryan','Brown','Bruce','Caleb','Cameron','Carl',
                'Carlos','Cary','Caspar','Cecil','Charles','Cheney','Chris','Christian','Christopher','Clark','Cliff','Cody','Cole','Colin','Cosmo','Daniel','Denny','Darwin','David','Dennis','Derek','Dick','Donald','Douglas','Duke','Dylan','Eddie','Edgar','Edison','Edmund','Edward','Edwin','Elijah','Elliott','Elvis','Eric','Frederick','Ethan','Eugene','Evan',
                'Enterprise','Ford','Francis','Frank','Francis','Franklin','Fred','Gabriel','Gaby','Gabriel','Garfield','Gary','Gavin','Geoffrey','George','Gino','Glen','Glendon',
                'Hank','Hardy','Harrison','Harry','Hayden','Henry','Hilton','Hugo','Hunk','Howard','Henry','Ian',
                'Ignativs','Ignace','Ignatz','Ivan','Isaac','Isaiah','Jack','Jackson','Jacob','James','Jason','Jay','Jeffery','Jerome','Jerry','Gerald','Jeremiah','Jerome','Jesse','Jim',
                'James','Jimmy','Joe','John','Johnny','Jonathan','Jordan','Joseph','Joshua','Justin','Keith','Ken','Kennedy','Kenneth','Kenny','Kevin','Kyle','Lance','Larry','Laurent','Lawrence','Leander','Lee','Leo','Leander','Leonard','Leopold','Leonard','Leopold','Leslie ','Loren','Lorry','Lorin','Louis','Luke','Marcus','Marcy','Mark','Marks','Mars','Marshal','Martin','Marvin','Mason','Matthew','Max','Michael','Mickey',
                'Mike','Nathan','Nathaniel','Neil','Nelson','Nicholas','Nick','Noah','Norman','Oliver','Oscar','Owen','Patrick','Paul','Peter','Philip','Phoebe','Quentin','Randal',
                'Randolph','Randy','Ray','Raymond','Reed','Rex','Richard','Richie','Rick','Ricky','Riley','Robert','Robin','Robinson','Rock','Roger','Ronald','Rowan','Roy','Ryan','Sam山','Sammy','Samuel','Scott','Sean','Shawn','Sidney','Simon','Solomon','Spark','Spencer','Spike','Stanley','Steve','Steven','Stewart','Stuart','Terence','Terry','Ted','Thomas','Tim','Timothy','Todd','Tommy','Tom','Thomas','Tony','Tyler','Ultraman','Ulysses','Van','Vern','Vernon','Victor','Vincent','Warner','Warren','Wayne','Wesley','William','Willy','Zack','Zachary']
        random_name =random.choice(namelist)
        last_name = random_name
        name = 'Jack ' + last_name

        self.data_fillInUserInfo = {
            "appId": param['appid'],
            "channelCode": param['channelcode'],
            "email": "jack@gmail.com",
            "education": "1",
            "firstName": "Jack ",
            "lastName": last_name,
            "birthday": "2001-02-01",
            "sex": "1",
            "marryStatus": "1",
            "city": ["Baringo", "Eldama Ravine"],
            "residenceStreet": "alick road no.40",
            "residenceProv": "Baringo",
            "residenceCity": "Eldama Ravine"
        }

        self.data_fillInUserInfo_mx = {
            "appId": param['appid'],
            "channelCode": param['channelcode'],
            "email": "jack@gmail.com",
            "education": 10,
            "name": name,
            "sex": 1,
            "birthday": "2001-02-01",
            "state": "MORELOS COA",
            "whatsApp": param['mobile'],
            "contacts": [
                {
                    "name": "Armender",
                    "mobile": "7021627172",
                    "relation": "PARENT",
                    "type": "family",
                    "error": {
                        "name": False,
                        "mobile": False
                    }
                },
                {
                    "name": "Apple Dheeraj",
                    "mobile": "8527293871",
                    "relation": "SISTER",
                    "type": "family",
                    "error": {
                        "name": False,
                        "mobile": False
                    }
                },
                {
                    "name": "Hector",
                    "mobile": "5578319167",
                    "relation": "FRIEND",
                    "type": "friendly",
                    "error": {
                        "name": False,
                        "mobile": False
                    }
                }
            ]
        }
        self.data_fillInUserInfo_co ={
            "appId": "${appId}",
            "channelCode": "${channelCode}",
            "email": "test@hotmail.com",
            "education": 1,
            "lastName": last_name,
            "name": "Jack",
            "sex": 1,
            "birthday": "2001-02-01",
            "state": "MORELOS COA",
            "contacts": [{
                "name": "Kevin Durant",
                "mobile": "3861534568",
                "relation": "SPOUSE",
                "type": "family",
                "error": {
                    "name": False,
                    "mobile": False,
                    "relation": False
                }
            }, {
                "name": "Kyrie Irving",
                "mobile": "3810669081",
                "relation": "PARENT",
                "type": "family",
                "error": {
                    "name": False,
                    "mobile": False,
                    "relation": False
                }
            }, {
                "name": "James Harden",
                "mobile": "3626821531",
                "relation": "FRIEND",
                "type": "friendly",
                "error": {
                    "name": False,
                    "mobile": False
                }
            }]
        }
        self.url_fillInUserInfo = 'http://' + param['url'] + '/app/api/multi/v2/user/fillInUserInfo/' + param['appid']

        # 保存联系人信息
        self.headers_saveContacts = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_saveContacts = {
            "contacts": [
                {
                    "mobile": "09528649368",
                    "name": "Alexa hard Rdd",
                    "relation": "PARENT"
                },
                {
                    "mobile": "09650790370",
                    "name": "Alto",
                    "relation": "PARENT"
                },
                {
                    "mobile": "09073220393",
                    "name": "Mike",
                    "relation": "FRIEND"
                }
            ],
            "devLatitudeX": 0,
            "devLongitudeX": 0,
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099306,
            "devLongitude": 113.309291,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }

        self.data_saveContacts_ke = {
            "contacts": [
                {
                    "mobile": "711649368",
                    "name": "Alexa hard Rdd",
                    "relation": "PARENT"
                },
                {
                    "mobile": "711649362",
                    "name": "Alto",
                    "relation": "PARENT"
                },
                {
                    "mobile": "758633766",
                    "name": "samxiang",
                    "relation": "FRIEND"
                }
            ],
            "devLatitudeX": 0,
            "devLongitudeX": 0,
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099306,
            "devLongitude": 113.309291,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }

        self.data_saveContacts_pk = {
            "contacts": [{
                "mobile": "9810669081",
                "name": "Kobe Bryant",
                "relation": "PARENT"
            }, {
                "mobile": "9990198551",
                "name": "LeBron James",
                "relation": "SPOUSE"
            }, {
                "mobile": "7586337662",
                "name": "Luka Dončić",
                "relation": "FRIEND"
            }],
            "devLatitudeX": 0,
            "devLongitudeX": 0,
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": "1.3.0.0",
            "brand": "vivo",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.0991485,
            "devLongitude": 113.309405,
            "devToken": "700fbe9dbda81fe12E:A6:00:93:C8:19",
            "gaid": "d268274b-e4bb-411a-bc55-a0b3e3edd42d",
            "language": "en-US",
            "mobileType": "1818",
            "os": "29",
            "osVersion": "10",
            "version": "1.3.0.0"
        }

        self.url_saveContacts = 'http://' + param['url'] + '/app/api/multi/v2/saveContacts/' + param['appid']

        # 创建预审订单
        self.headers_createApplyPreOrder = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_createApplyPreOrder = {
            "applySource": param['channelcode'],
            "loanDevInfo": {
                "appInstalledName": param['appid'],
                "brand": "Xiaomi",
                "callRecord": [
                    {
                        "callDate": "60",
                        "callSeconds": 20,
                        "contactName": "",
                        "contactPhone": param['mobile']
                    }
                ],
                "contactPhone": param['mobile'],
                "devIp": "8888",
                "devLatitude": 23.09395,
                "devLongitude": 113.316034,
                "devToken": "cb95881f542ac581",
                "devType": "andriod",
                "idfa": "1",
                "imei": "cb95881f542ac581",
                "isBreakPrison": 0,
                "isChangedAppSign": 0,
                "isNewAppVersion": 1,
                "isOpenGps": 1,
                "isPannel": 0,
                "isProxyIp": 0,
                "isRoot": 0,
                "isSimulator": 0,
                "isSupportCall": 1,
                "isWithBluetooth": 1,
                "latestRestartTime": "2021-03-27 21:31:10",
                "mobileType": "platina",
                "screenRatio": "",
                "sysVersion": "10",
                "totalMemory": 64,
                "twogIp": "",
                "udid": "cb95881f542ac581",
                "wifiAddr": "",
                "wifiLatitude": 23.09395,
                "wifiLongitude": 113.316034
            },
            "mobile": param['mobile'],
            "userId": param['userId'],
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.09395,
            "devLongitude": 113.316034,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }
        self.url_createApplyPreOrder = 'http://' + param['url'] + '/app/api/multi/v2/user/creatApplyPreOrder/' + param['appid']

        # 获取预审状态
        self.headers_getPreOrderStatus = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_getPreOrderStatus = {
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 0,
            "devLongitude": 0,
            "devToken": "",
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }
        self.url_getPreOrderStatus = 'http://' + param['url'] + '/app/api/multi/v2/user/getPreOrderStatus/' + param['appid']

        # 上传活体图片视频
        self.headers_uploadImages = {
            # 'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            # 'Content-Type': 'multipart/form-data; boundary=1ed0e7ca-a679-4ae9-9373-6937bc5cbd59',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.app_id = param['appid']
        self.url_uploadImages = 'http://' + param['url'] + '/app/api/multi/v2/uploadImages/' + param['appid']
        self.url_uploadImages_id = 'http://' + param['url'] + '/app/api/multi/v2/uploadIdCardImage/%s?appId=%s&picType=INE&livenessId=' % (
            self.app_id, self.app_id)
        self.url_uploadImages_mx = 'http://' + param['url'] + '/app/api/multi/v2/uploadIdCardImage/%s?appId=%s&picType=FACE&livenessId=' % (
            self.app_id, self.app_id)
        self.url_uploadImages_pk = 'http://' + param['url'] + '/app/api/multi/v2/uploadIdCardImage/%s?appId=%s&picType=AADHAAR&livenessId=' % (
            self.app_id, self.app_id)


        # 提交视频认证
        self.headers_video_certification = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_video_certification = {
            "appId": param['appid'],
            "readNumber": "3959",
            "videoUrl": param['mp4_url'],
        }
        self.url_video_certification = 'http://' + param['url'] + '/app/api/multi/v2/video-certification-submit'

        # curp 认证
        self. headers_curp_rfc_check = {
            'Host': param['authorization'],
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'http://172.20.240.121',
            'Accept-Language': param['language'],
            'Authorization': param['authorization'],
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
            'AppVersion': param['appversion'],
            'Referer': 'http://172.20.240.121/static/native_web/%s/' % (param['appid']),
            'X-Requested-With': param['appid']
        }

        self.data_curp_rfc_check = {
            "curp": 'MOHA741013MOCRRN04',
            "rfc": "MOHA741013MOC",
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099311,
            "devLongitude": 113.309342,
            "devToken": "f4ae3f8debcb939670:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "Android",
            "osVersion": "9",
            "version": param['appversion']
        }
        self.url_curp_rfc_check = 'http://' + param['url'] + '/app/api/multi/v2/user/curp-rfc-check/' + self.app_id

        # nga 绑卡认证
        self. headers_authBindRequest = {
            'Host': param['authorization'],
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'http://172.20.240.121',
            'Accept-Language': param['language'],
            'Authorization': param['authorization'],
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
            'AppVersion': param['appversion'],
            'Referer': 'http://172.20.240.121/static/native_web/%s/' % (param['appid']),
            'X-Requested-With': param['appid']
        }
        # bvn = str(int(time.time() * 10))
        self.cardNo = param['mobile']
        self.data_authBindRequest = {"appId": param['appid'],
                                "channelCode": param['channelcode'],
                                "bvn": '%s',
                                "cardNo": self.cardNo,
                                "bankCode": "801"}
        self.url_authBindRequest = 'http://' + param['url'] + '/app/api/multi/v2/user/authBindRequest/' + param['appid']

        # ke 绑卡参数
        self.band_card_date_ke = {
            "appId": param['appid'],
            "channelCode": param['channelcode'],
            "cardNo": param['mobile'],
            "smsCode": "123456"
        }
        self.data_sendSmsCode_band = {
            "appId": param['appid'],
            "channelCode": param['channelcode'],
            "mobile": param['mobile'],
            "loginType": "0",
            "language": "en_US",
            "smsCodeType": "BIND_MPESA"
        }
        # mx 绑卡
        self.headers_bind_card = {
            'accept': 'application/json',
            'appversion': param['appversion'],
            'devtoken': 'f4ae3f8debcb939670:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        # cardNo_mx = str(int(time.time()*100*100*100))
        self.cardNo_mx = '5579070118626178'
        self.data_bind_card = {
            "bankCode": "40112",
            "bindCardType": "0",
            "cardNo": self.cardNo_mx,
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.099311,
            "devLongitude": 113.309342,
            "devToken": "f4ae3f8debcb939670:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": "es-MX",
            "mobileType": "platina",
            "os": "Android",
            "osVersion": "9",
            "version": param['appversion'],
        }
        # 哥伦比亚不绑卡
        self.band_card_date_co = {
            "bankCode": "",
            "bindCardType": "1",
            "cardNo": "",
            "appId": "${appId}",
            "appName": "${appName}",
            "appPackageName": "${appPackageName}",
            "appVersion": "1.3.0.7",
            "brand": "motorola",
            "channelCode": "${channelCode}",
            "clientType": "ANDROID",
            "devLatitude": 0.0,
            "devLongitude": 0.0,
            "devToken": "eae1aad66929f3f00A:54:F6:A9:5A:4D",
            "gaid": "af8d8fe7-eeaa-49e9-ad0f-b7a38349a25f",
            "language": "es-MX",
            "mobileType": "foles_vzw",
            "os": "Android",
            "osVersion": "10",
            "version": "1.3.0.7"
        }
        #pk 绑卡参数
        self.band_card_date_pk = {
            "appId": "${appId}",
            "channelCode": "${channelCode}",
            "bankCode": "HBL",
            "cardNo": "346738638869988",
            "bindType": "1"

        }

        # 代扣支付认证
        # headers_authBindPaymentRequest = {
        #     'Host':  param['url'],
        #     'Pragma': 'no-cache',
        #     'Cache-Control': 'no-cache',
        #     'Origin': 'http://172.20.240.121',
        #     'Accept-Language': param['language'],
        #     'Authorization': param['authorization'],
        #     'Content-Type': 'application/json; charset=utf-8',
        #     'Accept': 'application/json',
        #     'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
        #     'AppVersion': param['appversion'],
        #     'Referer': 'http://172.20.240.121/static/native_web/%s/' % (param['appid']),
        #     'X-Requested-With': param['appid']
        # }
        # data_authBindPaymentRequest = {"appId": param['appid'],
        #                                "channelCode": param['channelcode'],
        #                                "bvn": bvn, "cardNo": cardNo, "bankCode": "801", "realName": "Alick Lee"}
        # url_authBindPaymentRequest = 'http://' + param['url'] + '/app/api/multi/v2/user/authBindPaymentRequest'

        # 申请进件接口
        self.headers_createApply = {
            'accept': 'application/json',
            'appversion': '1.3.0.0',
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Content-Type': 'application/json; charset=UTF-8',
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.data_createApply = {
            "amount": 1100,
            "applySource": param['appPackageName'],
            "loanDevInfo": {
                "appInstalledName": param['appid'],
                "brand": "Xiaomi",
                "callRecord": [
                    {
                        "callDate": "60",
                        "callSeconds": 20,
                        "contactName": "",
                        "contactPhone": param['mobile']
                    }
                ],
                "contactPhone": param['mobile'],
                "devIp": "8888",
                "devLatitude": 23.09395,
                "devLongitude": 113.316034,
                "devToken": "cb95881f542ac581",
                "devType": "andriod",
                "idfa": "1",
                "imei": "cb95881f542ac581",
                "isBreakPrison": 0,
                "isChangedAppSign": 0,
                "isNewAppVersion": 1,
                "isOpenGps": 1,
                "isPannel": 0,
                "isProxyIp": 0,
                "isRoot": 0,
                "isSimulator": 0,
                "isSupportCall": 1,
                "isWithBluetooth": 1,
                "latestRestartTime": "2021-03-27 21:31:10",
                "mobileType": "platina",
                "screenRatio": "",
                "sysVersion": "10",
                "totalMemory": 64,
                "twogIp": "",
                "udid": "cb95881f542ac581",
                "wifiAddr": "",
                "wifiLatitude": 23.09395,
                "wifiLongitude": 113.316034
            },
            "mobile": param['mobile'],
            "period": "1",
            "repayAndReloanFlag": 0,
            "userId": param['userId'],
            "appId": param['appid'],
            "appName": param['appname'],
            "appPackageName": param['appPackageName'],
            "appVersion": param['appversion'],
            "brand": "Xiaomi",
            "channelCode": param['channelcode'],
            "clientType": "ANDROID",
            "devLatitude": 23.09395,
            "devLongitude": 113.316034,
            "devToken": "cb95881f542ac58170:BB:E9:91:D3:CD",
            "gaid": "f1682b87-c032-4409-9272-0ad94548e5fa",
            "language": param['language'],
            "mobileType": "platina",
            "os": "28",
            "osVersion": "9",
            "version": param['appversion'],
        }
        self.url_createApply = 'http://' + param['url'] + '/app/api/multi/v2/user/creatApply/' + param['appid']

        # 获取订单id
        self.headers_getOrderDetail = {
            'accept': 'application/json',
            'content-type': 'application/json; charset=utf-8',
            'appversion': param['appversion'],
            'devtoken': 'cb95881f542ac58170:BB:E9:91:D3:CD',
            'authorization': param['authorization'],
            'accept-language': param['language'],
            'clientCode': param['clientcode'],
            'Host':  param['url'],
            'User-Agent': 'okhttp/4.9.0',
        }
        self.url_getOrderDetail = 'http://' + param['url'] + '/app/api/multi/v2/user/getOrderDetail/' + param['appid']

        # 复审回调通过
        self.headers_callback_order = {
            "Content-Type": "application/json"
        }
        self.data_callback_order = {
            "busOrderId": 'loan_order_id',
            "result": "agree"
        }
        self.url_callback_order = 'http://' + param['transfer_url']

        # 运营后台获取token
        self.headers_admin = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.data_admin = {
            'username': 'tanjiahua',
            'password': '123456',
            'grant_type': 'password'
        }
        self.url_admin = 'http://' + param['admin_web_url'] + '/oauth/token'

        # 运营后台点击放款
        self.headers_transfer = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'access_token'
        }
        self.data_transfer = {"loanOrderIds": ["loan_order_id"], "payChannel": "RAZOR"}
        self.url_transfer = 'http://' + param['admin_web_url'] + '/order/order/batchTransfer'

        # xxl-job login
        self.headers_job_login = {
            # 'Connection': 'keep-alive',
            # 'Accept': '*/*',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Origin': param['xxl_job'],
            # 'Referer': param['xxl_job'] + '/xxl-job-admin/toLogin',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.data_job_login = {
            'userName': 'admin',
            'password': '123456'
        }
        self.url_job_login = 'http://' + param['xxl_job'] + '/xxl-job-admin/login'

        # xxl-job 放款准备
        self.headers_job_pre = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Referer': param['admin_web_url'] + '/xxl-job-admin/jobinfo?jobGroup=11',
            # 'X-Requested-With': 'XMLHttpRequest',
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.data_job_pre = {
            'id': '19',
            'executorParam': ''
        }

        self.url_job_pre = 'http://' + param['xxl_job'] + '/xxl-job-admin/jobinfo/trigger'

        # xxl-job 完成放款
        self.headers_job_over = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://' + param['admin_web_url'] + '/xxl-job-admin/jobinfo?jobGroup=11',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        self.data_job_over = {
            'id': '18',
            'executorParam': ''
        }
        # 肯尼亚放款回调
        self.payoutNotify_ke = {
            "Result": {
                "ResultType": 0,
                "ResultCode": 0,
                "ResultDesc": "The service request is processed successfully.",
                "OriginatorConversationID": "10571-7910404-1",
                "ConversationID": "AG_20210721_000068264cb11a46e64d",
                "TransactionID": "NLJ41HAY6Q",
                "ResultParameters": {
                    "ResultParameter": [
                        {
                            "Key": "TransactionAmount",
                            "Value": 10
                        },
                        {
                            "Key": "TransactionReceipt",
                            "Value": "NLJ41HAY6Q"
                        },
                        {
                            "Key": "B2CRecipientIsRegisteredCustomer",
                            "Value": "Y"
                        },
                        {
                            "Key": "B2CChargesPaidAccountAvailableFunds",
                            "Value": -4510.00
                        },
                        {
                            "Key": "ReceiverPartyPublicName",
                            "Value": "254708374149 - John Doe"
                        },
                        {
                            "Key": "TransactionCompletedDateTime",
                            "Value": "19.12.2019 11:45:50"
                        },
                        {
                            "Key": "B2CUtilityAccountAvailableFunds",
                            "Value": 10116.00
                        },
                        {
                            "Key": "B2CWorkingAccountAvailableFunds",
                            "Value": 900000.00
                        }
                    ]
                },
                "ReferenceData": {
                    "ReferenceItem": {
                        "Key": "QueueTimeoutURL",
                        "Value": "https:\/\/internalsandbox.safaricom.co.ke\/mpesa\/b2cresults\/v1\/submit"
                    }
                }
            }
        }

        # 哥伦比亚放款回调
        self.payoutNotify_co ={
            "country": "Colombia",
            "lastName": "Gómez",
            "ticketNumber": "${third_trans_no}",
            "metadata": {
                "ref1": "Kushki test"
            },
            "documentType": "CC",
            "documentNumber": "123456789",
            "processorType": "gateway",
            "description": "Description of the payment",
            "merchantName": "Tu Gran Empresa",
            "processorId": "6000000000160XXXXXXXXXXXXX1786",
            "pin": "2087838888",
            "merchantId": "20000000XXXXXXXX2000",
            "currency": "COP",
            "processorName": "PuntoRed Processor",
            "email": "test Approved Tr",
            "amount": {
                "subtotalIva0": 50000,
                "iva": 0,
                "subtotalIva": 0
            },
            "completedAt": 1602087880267,
            "transactionStatus": "approvedTransaction",
            "created": 1602087815429,
            "kushkiAmount": 0,
            "transactionId": "eb41fa79-d936-4798-999a-001fc45767ab",
            "token": "0d951738a6094cd3bec5254dbe35b182",
            "transactionType": "PAYOUT",
            "totalAmount": 50000,
            "phoneNumber": "0934748855",
            "name": "Rafael",
            "paymentMethod": "cash",
            "expiration": 1602260615429,
            "transactionReference": "eb41fa79-d936-4798-999a-001fc45767ab"
        }

        self.url_job_over = 'http://' + param['xxl_job'] + '/xxl-job-admin/jobinfo/trigger'

        # d-2同步催收
        self.data_job_cs = {
            'id': '9',
            'executorParam': ''
        }

        self.data_job_overdue = {
            'id': '8',
            'executorParam': ''
        }

        self.assign_headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'access_token',
        }

        self.assign_data = {"dunAgencyId": "1", "dunGroupId": "1", "dunUserId": "1326", "loanOrderIds": "loan_order_id",
                       "assignType": "DUN_USER"}
        self.admin_web_assign = 'http://' + param['admin_web_url'] + '/dun/dun/order/assign'

        # 允许展期
        self.extension_headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'access_token',
        }

        self.extension_data = {"loanOrderId": "loan_order_id"}
        self.extension_url = 'http://' + param['admin_web_url'] + '/dun/dun/extension/apply'

        # 运营后台完成还款
        # 获取还款计划
        self.url_loanBillPlanId = 'http://' + param['admin_web_url'] + '/order/query/repayment/plan/detail'
        self.headers_loanBillPlanId = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'access_token'
        }
        self.data_loanBillPlanId = {"loanOrderId": "loan_order_id"}

        # 执行还款
        self.url_repay = 'http://' + param['admin_web_url'] + '/order/offline/repayment'
        self.headers_repay = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'access_token'
        }
        self.data_repay = {"repayTime":time.strftime("%Y-%m-%d %H:%I:%S", time.localtime( time.time() ) ),
                           "applyReductionAmount":0,
                           "amount":"repay_amount",
                           "thirdOrderId": "loan_order_id",
                           "fileUrl":"",
                           "loanBillPlanId":'loan_BillPlan_Id'}

        # 返回字典参数
        key = [  'url_checkUserExist','headers_checkUserExist', 'data_checkUserExist',
                 'url_sendSmsCode','headers_sendSmsCode','data_sendSmsCode',
                 'url_userRegister', 'headers_userRegister', 'data_userRegister',
                 'url_sendloginSmsCode', 'headers_sendloginSmsCode', 'data_sendloginSmsCode',
                 'url_smslogin', 'headers_smslogin', 'data_smslogin',
                 'url_fillInUserInfo', 'headers_fillInUserInfo', 'data_fillInUserInfo_mx','data_fillInUserInfo',
                 'data_fillInUserInfo_co',
                 'url_saveContacts', 'headers_saveContacts', 'data_saveContacts_ke', 'data_saveContacts','data_saveContacts_pk',
                 'url_createApplyPreOrder', 'headers_createApplyPreOrder', 'data_createApplyPreOrder',
                 'url_getPreOrderStatus', 'headers_getPreOrderStatus', 'data_getPreOrderStatus',
                 'url_uploadImages_pk','url_uploadImages_mx','url_uploadImages_id','url_uploadImages','app_id','headers_uploadImages',
                 'url_video_certification','headers_video_certification','data_video_certification',
                 'url_curp_rfc_check','headers_curp_rfc_check','data_curp_rfc_check',
                 'url_authBindRequest','headers_authBindRequest','data_authBindRequest','cardNo',
                 'band_card_date_ke','data_sendSmsCode_band','headers_bind_card','cardNo_mx','data_bind_card',
                 'band_card_date_co','band_card_date_pk',
                 'url_createApply','headers_createApply','data_createApply',
                 'url_getOrderDetail','headers_getOrderDetai',
                 'url_callback_order','headers_callback_order','data_callback_order',
                 'url_admin','headers_admin','data_admin',
                 'url_transfer','headers_transfer','data_transfer',
                 'url_job_login','headers_job_login','data_job_login',
                 'url_job_pre','headers_job_pre','data_job_pre',
                 'url_job_over','headers_job_over','data_job_over','payoutNotify_ke',
                 'payoutNotify_co',
                 'url_loanBillPlanId','headers_loanBillPlanId','data_loanBillPlanId',
                 'url_repay','headers_repay','data_repay']
        value = [self.url_checkUserExist,self.headers_checkUserExist, self.data_checkUserExist,
                 self.url_sendSmsCode,self.headers_sendSmsCode,self.data_sendSmsCode,
                 self.url_userRegister, self.headers_userRegister, self.data_userRegister,
                 self.url_sendloginSmsCode, self.headers_sendloginSmsCode, self.data_sendloginSmsCode,
                 self.url_smslogin, self.headers_smslogin, self.data_smslogin,
                 self.url_fillInUserInfo, self.headers_fillInUserInfo, self.data_fillInUserInfo_mx,self.data_fillInUserInfo,
                 self.data_fillInUserInfo_co,
                 self.url_saveContacts, self.headers_saveContacts, self.data_saveContacts_ke, self.data_saveContacts,self.data_saveContacts_pk,
                 self.url_createApplyPreOrder, self.headers_createApplyPreOrder, self.data_createApplyPreOrder,
                 self.url_getPreOrderStatus, self.headers_getPreOrderStatus, self.data_getPreOrderStatus,
                 self.url_uploadImages_pk,self.url_uploadImages_mx,self.url_uploadImages_id,self.url_uploadImages,self.app_id,self.headers_uploadImages,
                 self.url_video_certification,self.headers_video_certification,self.data_video_certification,
                 self.url_curp_rfc_check,self.headers_curp_rfc_check,self.data_curp_rfc_check,
                 self.url_authBindRequest,self. headers_authBindRequest,self.data_authBindRequest,self.cardNo,
                 self.band_card_date_ke,self.data_sendSmsCode_band,self.headers_bind_card,self.cardNo_mx,self.data_bind_card,
                 self.band_card_date_co,self.band_card_date_pk,
                 self.url_createApply,self.headers_createApply,self.data_createApply,
                 self.url_getOrderDetail,self.headers_getOrderDetail,
                 self.url_callback_order,self.headers_callback_order,self.data_callback_order,
                 self.url_admin,self.headers_admin,self.data_admin,
                 self.url_transfer,self.headers_transfer,self.data_transfer,
                 self.url_job_login,self.headers_job_login,self.data_job_login,
                 self.url_job_pre,self.headers_job_pre,self.data_job_pre,
                 self.url_job_over,self.headers_job_over,self.data_job_over,self.payoutNotify_ke,
                 self.payoutNotify_co,
                 self.url_loanBillPlanId,self.headers_loanBillPlanId,self.data_loanBillPlanId,
                 self.url_repay,self.headers_repay,self.data_repay
                 ]
        data = dict( zip( key, value ) )
        return data