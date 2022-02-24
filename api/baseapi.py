# !/usr/local/python3
# -*- coding:utf-8 -*-
# Date      :2021/3/27
# FileName  :baseapi.py
# Describe  :
# Author    :jack
import importlib
import os
import random
import string
import time
import traceback
from configparser import RawConfigParser
from pymongo import MongoClient
import datetime
from requests.auth import HTTPDigestAuth
from common import logging_func
from common import params_init as p
from common import test_mysql as db
import json
import requests
from rediscluster import RedisCluster
log = logging_func.Logger().logger
path = os.path.dirname(os.path.abspath(__file__))


class BaseApi(object):
    def __init__(self, env_mark, test_ini, sql_ini, app_name):
        self.env_mark = env_mark
        self.test_ini = test_ini
        self.sql_ini = sql_ini
        self.cfg_sql_ini = self.read_ini(self.sql_ini)
        self.cfg_test_ini = self.read_ini(self.test_ini)
        self.param = 'global_param_' + app_name
        self.app_name = app_name

    @staticmethod
    def read_ini(filename):
        cfg_test_ini = RawConfigParser()
        cfg_test_ini.read(path + '/config_ini/' + filename)
        return cfg_test_ini

    @staticmethod
    def delete_redis_key():
        conn_list = [
            {"host": "172.20.240.45", "port": "2001"},
            {"host": "172.20.240.45", "port": "2002"},
            {"host": "172.20.240.45", "port": "2003"},
            {"host": "172.20.240.45", "port": "2004"},
            {"host": "172.20.240.45", "port": "2005"},
            {"host": "172.20.240.45", "port": "2006"}
        ]

        con_redis = RedisCluster(startup_nodes=conn_list, password='testmx123456', decode_responses=True)
        key = '"mx:cfs:user:userid:'
        keys = con_redis.scan_iter(match=f"*{key}*")
        for key in keys:
            log.info('删除redis key' + f": {key}")
            con_redis.delete(f"{key}")

    def new_mobile(self):
        if self.env_mark == 'nga':
            mobile = '0' + str(int(time.time()))
            # mobile=mobile_num
        elif self.env_mark == 'mx':
            mobile = str(int(time.time()))
            # mobile=mobile_num
            self.delete_redis_key()
            sql = self.cfg_sql_ini.get('user_id_card', 'id_card_1') % mobile
            sql_1 = self.cfg_sql_ini.get('user_id_card', 'id_card_2') % mobile
            user = db.update(sql, self.env_mark)
            order = db.update(sql_1, self.env_mark)
            log.info('更新脏数据%s条' % str(user + order))
        elif self.env_mark == 'ke':
            mobile = '7' + str(int(time.time()))[2:]
        elif self.env_mark == 'co':
            mobile = '3' + str(int(time.time()))[1:]
        elif self.env_mark == 'pk':
            mobile = str(int(time.time()))
        self.cfg_test_ini.set(self.param, 'mobile', mobile)
        self.cfg_test_ini.write(open(path + '/config_ini/' + self.test_ini, 'r+', encoding='utf-8'))
        log.info('======【%s测试环境】生成手机号：%s ======' % (self.env_mark, mobile))
        return mobile

    def register(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data(self,mark,param)
        mobile = data['data_checkUserExist']['mobile']
        register_url = data['url_checkUserExist']
        register_headers = data['headers_checkUserExist']
        register_data = json.dumps(data['data_checkUserExist'])
        res_check = requests.post(register_url, headers=register_headers, data=register_data)
        if '0000' in res_check.text:
            log.info('%s 检测用户存在成功！' % mobile)
        else:
            log.error('%s 检测用户存在失败！' % res_check.text)
            self.mobile()
        sendSmsCode_url = data['url_sendSmsCode']
        sendSmsCode_headers = data['headers_sendSmsCode']
        sendSmsCode_data = json.dumps( data['data_sendSmsCode'] )
        res_sms = requests.post(sendSmsCode_url, headers=sendSmsCode_headers, data=sendSmsCode_data)
        if '0000' in res_sms.text:
            log.info('%s 短信发送成功！' % mobile)
        else:
            log.error('%s 短信发送失败！' % res_sms.text)
        userRegister_url = data['url_userRegister']
        userRegister_headers=data['headers_userRegister']
        userRegister_data = json.dumps( data['data_userRegister'] )
        if self.env_mark == 'nga':
            userRegister_data = userRegister_data.replace('49283', '13416')
        else:
            userRegister_data = userRegister_data
        res_register = requests.post(userRegister_url, headers=userRegister_headers,
                                     data=userRegister_data)
        if '0000' in res_register.text:
            log.info('%s 注册成功！' % mobile)
        else:
            log.error('注册失败！%s' % userRegister_headers)
            log.error(res_register.text)
        return mobile

    def login(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        mobile = data['data_checkUserExist']['mobile']
        url_sendloginSmsCode=data['url_sendloginSmsCode']
        headers_sendloginSmsCode=data['headers_sendloginSmsCode']
        data_sendloginSmsCode=json.dumps( data['data_sendloginSmsCode'] )
        res_sms = requests.post( url_sendloginSmsCode, headers=headers_sendloginSmsCode, data=data_sendloginSmsCode )
        if '0000' in res_sms.text:
            log.info( '%s 登录短信发送成功！' % mobile )
        else:
            log.error( '%s 登录短信发送失败！' % res_sms.text )
        url_smslogin =data['url_smslogin']
        headers_smslogin = data['headers_smslogin']
        data_smslogin = json.dumps(data['data_smslogin'])
        res_login = requests.post(url_smslogin, headers=headers_smslogin, data=data_smslogin)
        if '0000' in res_login.text:
            token = res_login.json()['data']['token']
            user_id = res_login.json()['data']['userId']
            log.info('userId=%s,mobile=%s,token=%s 登录成功' % (user_id, mobile, token))
            self.cfg_test_ini.set(self.param, 'userid', user_id)
            self.user_id = user_id
            self.cfg_test_ini.set(self.param, 'authorization', token)
            self.cfg_test_ini.write(open(path + '/config_ini/%s' % self.test_ini, 'r+', encoding='utf-8'))
            # time.sleep(0.5)
        else:
            log.error('登录失败!')

    def insert_sdk_data(self):
        if self.env_mark == 'nga':
            my_client = MongoClient("mongodb://172.20.240.225:27017/")
            my_db = my_client.get_database("nga_sdk_pro")
        elif self.env_mark == 'mx':
            my_client = MongoClient("mongodb://172.20.240.45:27017/")
            my_db = my_client.get_database("mx_sdk_pro")
        elif self.env_mark == 'ke':
            my_client = MongoClient("mongodb://172.20.240.133:27017/")
            my_db = my_client.get_database("ke_sdk_pro")
        elif self.env_mark == 'co':
            my_client = MongoClient( "mongodb://172.20.240.255:27017/" )
            my_db = my_client.get_database( "co_sdk_pro" )
            return
        data1 = {
            "userId": self.user_id,
            "sdkType": "5",
            "batchNumber": "NDE2ODNkNjQtY2JlNi00MDVhLWJmN2ItZGUwZmM1ZTRkZjUz",
            "createTime": datetime.datetime.strptime("2021-07-01T11:21:02.316Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "updateTime": datetime.datetime.strptime("2021-07-01T11:21:02.316Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
            "appKey": "app-nga-biz-004",
            "dataCount": 100
        }

        my_col = my_db['sdk_first_upload_result']
        data_list = []
        for type in ['1', '2', '4', '5']:
            data1['sdkType'] = type
            data_list.append(data1.copy())
        my_col.insert_many(data_list)
        log.info('{%s}风控云数据记录插入mongo成功！' % self.user_id)

    def submit_user_ext_contacts(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        if self.env_mark == 'nga':
            data1 = json.dumps(data['data_fillInUserInfo'])
        elif self.env_mark == 'mx':
            data1 = json.dumps(data['data_fillInUserInfo_mx'])
        elif self.env_mark == 'co':
            data1 = json.dumps( data['data_fillInUserInfo_co'] )
        elif self.env_mark == 'pk':
            data1 = json.dumps( data['data_fillInUserInfo'] )
        elif self.env_mark == 'ke':
            nin = str(int(time.time()))[2:]
            ninFrontUrl = "http://172.20.240.138:8002/file/v1/fud/pri/pic/f2fe31e34cad4004b69cec74ea4bf505.jpeg"
            ninBackUrl = "http://172.20.240.138:8002/file/v1/fud/pri/pic/6c89fb07d67242159be2bf45d699c32d.jpeg"

            data['data_fillInUserInfo'].update(nin=nin)
            data['data_fillInUserInfo']['ninFrontUrl'] = ninFrontUrl
            data['data_fillInUserInfo']['ninBackUrl'] = ninBackUrl
            data1 = json.dumps(data['data_fillInUserInfo'])
        url_fillInUserInfo = data['url_fillInUserInfo']
        headers_fillInUserInfo = data['headers_fillInUserInfo']
        data_fillInUserInfo= data1
        res_fillInUserInfo = requests.post(url_fillInUserInfo, headers=headers_fillInUserInfo, data=data_fillInUserInfo)
        if '0000' in res_fillInUserInfo.text:
            log.info('个人信息提交成功！')
        else:
            log.error('个人信息提交失败！')
        if self.env_mark == 'mx' or self.env_mark == 'co':
            pass
        elif self.env_mark == 'nga':
            url_saveContacts = data['url_saveContacts']
            headers_saveContacts =data['headers_saveContacts']
            data_saveContacts = json.dumps( data['data_saveContacts'] )
            res_saveContacts = requests.post(url_saveContacts, headers=headers_saveContacts, data=data_saveContacts)
            if '0000' in res_saveContacts.text:
                log.info('联系人信息提交成功！')
            else:
                log.error('联系人信息提交失败！')
        elif self.env_mark == 'ke':
            url_saveContacts = data['url_saveContacts']
            headers_saveContacts =data['headers_saveContacts']
            data_saveContacts = json.dumps( data['data_saveContacts_ke'] )
            res_saveContacts = requests.post(url_saveContacts, headers=headers_saveContacts, data=data_saveContacts)
            if '0000' in res_saveContacts.text:
                log.info('联系人信息提交成功！')
            else:
                log.error('联系人信息提交失败！')
        elif self.env_mark == 'pk':
            url_saveContacts = data['url_saveContacts']
            headers_saveContacts =data['headers_saveContacts']
            data_saveContacts = json.dumps( data['data_saveContacts_pk'] )
            res_saveContacts = requests.post(url_saveContacts, headers=headers_saveContacts, data=data_saveContacts)
            if '0000' in res_saveContacts.text:
                log.info('联系人信息提交成功！')
            else:
                log.error('联系人信息提交失败！')


    def create_pre_order(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_createApplyPreOrder = data['url_createApplyPreOrder']
        headers_createApplyPreOrder = data['headers_createApplyPreOrder']
        data_createApplyPreOrder = json.dumps(data['data_createApplyPreOrder'])
        res_createApplyPreOrder = requests.post(url_createApplyPreOrder, headers=headers_createApplyPreOrder, data=data_createApplyPreOrder)
        if 'Successful' in res_createApplyPreOrder.text:
            log.info('创建预审订单成功！')
        else:
            log.error('创建预审失败%s' % res_createApplyPreOrder.text)

    def modify_pre_order_status(self):
        importlib.reload(db)
        sql = self.cfg_sql_ini.get('pre_order_update', 'pre_order_status') % self.user_id
        a = db.update(sql, self.env_mark)
        log.info('预审状态修改为通过,更新条数 %s' % a)
        sql = self.cfg_sql_ini.get('pre_order_update', 'init_user_quota') % self.user_id
        b = db.update(sql, self.env_mark)
        log.info('更新初始额度！更新条数 %s' % b)

    def upload_image(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        if self.env_mark == 'pk':
            id_card = [
                ('image', ('mx_curp_front.png', open(path+'config_ini/mx_id_card/mx_curp_front.png', 'rb'), 'image/png')),
                ('image', ('mx_curp_back.png', open(path+'config_ini/mx_id_card/mx_curp_back.png', 'rb'), 'image/png'))]
            url_uploadImages_id = data['url_uploadImages_pk']
            headers_uploadImages = data['headers_uploadImages']
            res_upload_image = requests.post(url_uploadImages_id, headers=headers_uploadImages, files=id_card)
            if 'Successful' in res_upload_image.text:
                log.info('curp上传成功!')
            else:
                log.error('curp上传失败!')
            id_card_no = res_upload_image.json()['data']['idCard']
            url_curp_rfc_check = data['url_curp_rfc_check']
            headers_curp_rfc_check = data['headers_curp_rfc_check']
            data_curp_rfc_check = json.dumps(data['data_curp_rfc_check']).replace('id_card_no', id_card_no)
            res_curp_rfc_check = requests.post(url_curp_rfc_check, headers=headers_curp_rfc_check, data=data_curp_rfc_check)
            if '0000' in res_curp_rfc_check.text:
                log.info('curp_rfc校验通过！')
                mobile = str(int(time.time()))
                appId = self.cfg_test_ini.get( self.param, 'appId' )
                channelCode = self.cfg_test_ini.get( self.param, 'channelCode' )
                # random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
                # id_card_1 = 'ALICKTEST00' + random_str
                id_card_1 = self.cfg_test_ini.get( self.param, 'mobile' )
                sql_tmp = self.cfg_sql_ini.get( 'user_id_card', 'id_card' )
                sql = sql_tmp % (name, id_card_1, mobile, appId, channelCode)
                db.update( sql, self.env_mark )
            else:
                log.error('curp_rfc校验失败！')
        elif self.env_mark == 'co':
            id_card = [
                ('image', ('mx_curp_front.png', open( '../config_ini/mx_id_card/mx_curp_front.png', 'rb' ), 'image/png')),
                ('image', ('mx_curp_back.png', open( '../config_ini/mx_id_card/mx_curp_back.png', 'rb' ), 'image/png'))]
            url_uploadImages_id = data['url_uploadImages_id']
            headers_uploadImages = data['headers_uploadImages']
            res_upload_image = requests.post(url_uploadImages_id, headers=headers_uploadImages, files=id_card)
            if 'Successful' in res_upload_image.text:
                log.info('curp上传成功!')
            else:
                log.error('curp上传失败!')
            id_card_no = res_upload_image.json()['data']['idCard']
            url_curp_rfc_check = data['url_curp_rfc_check']
            headers_curp_rfc_check = data['headers_curp_rfc_check']
            data_curp_rfc_check = json.dumps(data['data_curp_rfc_check']).replace('id_card_no', id_card_no)
            res_curp_rfc_check = requests.post(url_curp_rfc_check, headers=headers_curp_rfc_check, data=data_curp_rfc_check)
            if '0000' in res_curp_rfc_check.text:
                log.info('curp_rfc校验通过！')
                mobile = self.cfg_test_ini.get( self.param, 'mobile' )
                appId = self.cfg_test_ini.get( self.param, 'appId' )
                channelCode = self.cfg_test_ini.get( self.param, 'channelCode' )
                # random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
                # id_card_1 = 'ALICKTEST00' + random_str
                id_card_1 = self.cfg_test_ini.get( self.param, 'mobile' )
                sql_tmp = self.cfg_sql_ini.get( 'user_id_card', 'user' )
                sql = sql_tmp % (id_card_1, mobile, appId, channelCode)
                db.update( sql, self.env_mark )
            else:
                log.error('curp_rfc校验失败！')
        # 录制视频，上传
        if self.env_mark == 'nga' or self.env_mark == 'ke' or self.env_mark == 'co' or self.env_mark == 'pk':
            files = {"image": open( '../config_ini/face.mp4', 'rb' ), "Content-Type": "multipart/form-data",
                     "filename": "audio-1616915206998.mp4"}
            url_uploadImages = data['url_uploadImages']
            headers_uploadImages =data['headers_uploadImages']
            res_upload_mp4 = requests.post(url_uploadImages, headers=headers_uploadImages, files=files,
                                           verify=False)
            mp4_url = json.loads(res_upload_mp4.text)['data'][0]['outerUrl']
            if 'Successful' in res_upload_mp4.text:
                self.cfg_test_ini.set(self.param, 'mp4_url', mp4_url)
                self.cfg_test_ini.write(open(path + '/config_ini/%s' % self.test_ini, 'r+', encoding='utf-8'))
                log.info('活体图片上传成功！回写配置文件global_param.mp4_url')
            else:
                log.error('活体图片上传失败！')
                log.error(res_upload_mp4.text)
            importlib.reload(p)
            url_video_certification = data['url_video_certification']
            headers_video_certification = data['headers_video_certification']
            data = json.dumps(data['data_video_certification'])
            res_video_certification = requests.post(url_video_certification, headers=headers_video_certification, data=data)
            if 'Successful' in res_video_certification.text:
                log.info('视频认证通过！')
        elif self.env_mark == 'mx':
            id_card = [
                ('image', ('mx_curp_front.png', open( '../config_ini/mx_id_card/mx_curp_front.png', 'rb' ), 'image/png')),
                ('image', ('mx_curp_back.png', open( '../config_ini/mx_id_card/mx_curp_back.png', 'rb' ), 'image/png'))]
            url_uploadImages_id = data['url_uploadImages_id']
            headers_uploadImages = data['headers_uploadImages']
            res_upload_image = requests.post(url_uploadImages_id, headers=headers_uploadImages, files=id_card)
            if 'Successful' in res_upload_image.text:
                log.info('curp上传成功!')
            else:
                log.error('curp上传失败!')
            id_card_no = res_upload_image.json()['data']['idCard']
            url_curp_rfc_check = data['url_curp_rfc_check']
            headers_curp_rfc_check = data['headers_curp_rfc_check']
            data_curp_rfc_check = json.dumps(data['data_curp_rfc_check']).replace('id_card_no', id_card_no)
            res_curp_rfc_check = requests.post(url_curp_rfc_check, headers=headers_curp_rfc_check, data=data_curp_rfc_check)
            if '0000' in res_curp_rfc_check.text:
                log.info('curp_rfc校验通过！')
            else:
                log.error('curp_rfc校验失败！')
            file_face = {"image": open( '../config_ini/mx_face.jpeg', 'rb' ),
                         "Content-Type": "multipart/form-data",
                         "filename": "1617112538067.jpg"}
            url_uploadImages_mx = data['url_uploadImages_mx']
            headers_uploadImages = data['headers_uploadImages']
            res_upload_face = requests.post(url_uploadImages_mx, headers=headers_uploadImages, files=file_face,
                                            verify=False)
            if 'Successful' in res_upload_face.text:
                log.info('人脸识别成功!')
                namelist = ['Aaron', 'Abe', 'Abelard', 'Abraham', 'Adam', 'Adrian', 'Aidan', 'Alva', 'Alex',
                            'Alexander', 'Alan', 'Eilian', 'Ailin', 'Albert', 'Alfred', 'Andrew', 'Andy', 'Angus',
                            'Anthony', 'Apollo', 'Arnold', 'Arthur', 'August', 'Austin', 'Ben', 'Benjamin', 'Bert',
                            'Benson', 'Bill', 'Billy', 'Blake', 'Bob', 'Bobby', 'Brad', 'Brandon', 'Brant', 'Brent',
                            'Bryan', 'Brown', 'Bruce', 'Caleb', 'Cameron', 'Carl',
                            'Carlos', 'Cary', 'Caspar', 'Cecil', 'Charles', 'Cheney', 'Chris', 'Christian',
                            'Christopher', 'Clark', 'Cliff', 'Cody', 'Cole', 'Colin', 'Cosmo', 'Daniel', 'Denny',
                            'Darwin', 'David', 'Dennis', 'Derek', 'Dick', 'Donald', 'Douglas', 'Duke', 'Dylan', 'Eddie',
                            'Edgar', 'Edison', 'Edmund', 'Edward', 'Edwin', 'Elijah', 'Elliott', 'Elvis', 'Eric',
                            'Frederick', 'Ethan', 'Eugene', 'Evan',
                            'Enterprise', 'Ford', 'Francis', 'Frank', 'Francis', 'Franklin', 'Fred', 'Gabriel', 'Gaby',
                            'Gabriel', 'Garfield', 'Gary', 'Gavin', 'Geoffrey', 'George', 'Gino', 'Glen', 'Glendon',
                            'Hank', 'Hardy', 'Harrison', 'Harry', 'Hayden', 'Henry', 'Hilton', 'Hugo', 'Hunk', 'Howard',
                            'Henry', 'Ian',
                            'Ignativs', 'Ignace', 'Ignatz', 'Ivan', 'Isaac', 'Isaiah', 'Jack', 'Jackson', 'Jacob',
                            'James', 'Jason', 'Jay', 'Jeffery', 'Jerome', 'Jerry', 'Gerald', 'Jeremiah', 'Jerome',
                            'Jesse', 'Jim',
                            'James', 'Jimmy', 'Joe', 'John', 'Johnny', 'Jonathan', 'Jordan', 'Joseph', 'Joshua',
                            'Justin', 'Keith', 'Ken', 'Kennedy', 'Kenneth', 'Kenny', 'Kevin', 'Kyle', 'Lance', 'Larry',
                            'Laurent', 'Lawrence', 'Leander', 'Lee', 'Leo', 'Leander', 'Leonard', 'Leopold', 'Leonard',
                            'Leopold', 'Leslie ', 'Loren', 'Lorry', 'Lorin', 'Louis', 'Luke', 'Marcus', 'Marcy', 'Mark',
                            'Marks', 'Mars', 'Marshal', 'Martin', 'Marvin', 'Mason', 'Matthew', 'Max', 'Michael',
                            'Mickey',
                            'Mike', 'Nathan', 'Nathaniel', 'Neil', 'Nelson', 'Nicholas', 'Nick', 'Noah', 'Norman',
                            'Oliver', 'Oscar', 'Owen', 'Patrick', 'Paul', 'Peter', 'Philip', 'Phoebe', 'Quentin',
                            'Randal',
                            'Randolph', 'Randy', 'Ray', 'Raymond', 'Reed', 'Rex', 'Richard', 'Richie', 'Rick', 'Ricky',
                            'Riley', 'Robert', 'Robin', 'Robinson', 'Rock', 'Roger', 'Ronald', 'Rowan', 'Roy', 'Ryan',
                            'Sam山', 'Sammy', 'Samuel', 'Scott', 'Sean', 'Shawn', 'Sidney', 'Simon', 'Solomon', 'Spark',
                            'Spencer', 'Spike', 'Stanley', 'Steve', 'Steven', 'Stewart', 'Stuart', 'Terence', 'Terry',
                            'Ted', 'Thomas', 'Tim', 'Timothy', 'Todd', 'Tommy', 'Tom', 'Thomas', 'Tony', 'Tyler',
                            'Ultraman', 'Ulysses', 'Van', 'Vern', 'Vernon', 'Victor', 'Vincent', 'Warner', 'Warren',
                            'Wayne', 'Wesley', 'William', 'Willy', 'Zack', 'Zachary']
                random_name = random.choice( namelist )
                name = 'Jack ' + random_name
                mobile = self.cfg_test_ini.get(self.param, 'mobile')
                appId = self.cfg_test_ini.get(self.param, 'appId')
                channelCode = self.cfg_test_ini.get(self.param, 'channelCode')
                # random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
                # id_card_1 = 'ALICKTEST00' + random_str
                id_card_1 = 'GEML' + self.cfg_test_ini.get(self.param, 'mobile') + 'YY'
                sql_tmp = self.cfg_sql_ini.get('user_id_card', 'id_card')
                sql = sql_tmp % (name, id_card_1, mobile, appId, channelCode)
                db.update(sql, self.env_mark)
            else:
                log.error('人脸识别失败%s' % res_upload_face.text)

        elif self.env_mark == 'pk':
            id_card = [
                ('image', ('mx_curp_front.png', open( '../config_ini/mx_id_card/mx_curp_front.png', 'rb' ), 'image/png')),
                ('image', ('mx_curp_back.png', open( '../config_ini/mx_id_card/mx_curp_back.png', 'rb' ), 'image/png'))]
            importlib.reload( p )
            mark = self.env_mark
            param = self.param
            data = p.loan_data.return_data( self, mark, param )
            url_uploadImages_id = data['url_uploadImages_pk']
            headers_uploadImages = data['headers_uploadImages']
            res_upload_image = requests.post(url_uploadImages_id, headers=headers_uploadImages, files=id_card)
            if 'Successful' in res_upload_image.text:
                log.info('curp上传成功!')
            else:
                log.error('curp上传失败!')
            id_card_no = res_upload_image.json()['data']['idCard']
            url_curp_rfc_check = data['url_curp_rfc_check']
            headers_curp_rfc_check = data['headers_curp_rfc_check']
            data_curp_rfc_check = json.dumps(data['data_curp_rfc_check']).replace('id_card_no', id_card_no)
            res_curp_rfc_check = requests.post(url_curp_rfc_check, headers=headers_curp_rfc_check, data=data_curp_rfc_check)
            if '0000' in res_curp_rfc_check.text:
                log.info('curp_rfc校验通过！')
                namelist = ['Aaron', 'Abe', 'Abelard', 'Abraham', 'Adam', 'Adrian', 'Aidan', 'Alva', 'Alex',
                            'Alexander', 'Alan', 'Eilian', 'Ailin', 'Albert', 'Alfred', 'Andrew', 'Andy', 'Angus',
                            'Anthony', 'Apollo', 'Arnold', 'Arthur', 'August', 'Austin', 'Ben', 'Benjamin', 'Bert',
                            'Benson', 'Bill', 'Billy', 'Blake', 'Bob', 'Bobby', 'Brad', 'Brandon', 'Brant', 'Brent',
                            'Bryan', 'Brown', 'Bruce', 'Caleb', 'Cameron', 'Carl',
                            'Carlos', 'Cary', 'Caspar', 'Cecil', 'Charles', 'Cheney', 'Chris', 'Christian',
                            'Christopher', 'Clark', 'Cliff', 'Cody', 'Cole', 'Colin', 'Cosmo', 'Daniel', 'Denny',
                            'Darwin', 'David', 'Dennis', 'Derek', 'Dick', 'Donald', 'Douglas', 'Duke', 'Dylan', 'Eddie',
                            'Edgar', 'Edison', 'Edmund', 'Edward', 'Edwin', 'Elijah', 'Elliott', 'Elvis', 'Eric',
                            'Frederick', 'Ethan', 'Eugene', 'Evan',
                            'Enterprise', 'Ford', 'Francis', 'Frank', 'Francis', 'Franklin', 'Fred', 'Gabriel', 'Gaby',
                            'Gabriel', 'Garfield', 'Gary', 'Gavin', 'Geoffrey', 'George', 'Gino', 'Glen', 'Glendon',
                            'Hank', 'Hardy', 'Harrison', 'Harry', 'Hayden', 'Henry', 'Hilton', 'Hugo', 'Hunk', 'Howard',
                            'Henry', 'Ian',
                            'Ignativs', 'Ignace', 'Ignatz', 'Ivan', 'Isaac', 'Isaiah', 'Jack', 'Jackson', 'Jacob',
                            'James', 'Jason', 'Jay', 'Jeffery', 'Jerome', 'Jerry', 'Gerald', 'Jeremiah', 'Jerome',
                            'Jesse', 'Jim',
                            'James', 'Jimmy', 'Joe', 'John', 'Johnny', 'Jonathan', 'Jordan', 'Joseph', 'Joshua',
                            'Justin', 'Keith', 'Ken', 'Kennedy', 'Kenneth', 'Kenny', 'Kevin', 'Kyle', 'Lance', 'Larry',
                            'Laurent', 'Lawrence', 'Leander', 'Lee', 'Leo', 'Leander', 'Leonard', 'Leopold', 'Leonard',
                            'Leopold', 'Leslie ', 'Loren', 'Lorry', 'Lorin', 'Louis', 'Luke', 'Marcus', 'Marcy', 'Mark',
                            'Marks', 'Mars', 'Marshal', 'Martin', 'Marvin', 'Mason', 'Matthew', 'Max', 'Michael',
                            'Mickey',
                            'Mike', 'Nathan', 'Nathaniel', 'Neil', 'Nelson', 'Nicholas', 'Nick', 'Noah', 'Norman',
                            'Oliver', 'Oscar', 'Owen', 'Patrick', 'Paul', 'Peter', 'Philip', 'Phoebe', 'Quentin',
                            'Randal',
                            'Randolph', 'Randy', 'Ray', 'Raymond', 'Reed', 'Rex', 'Richard', 'Richie', 'Rick', 'Ricky',
                            'Riley', 'Robert', 'Robin', 'Robinson', 'Rock', 'Roger', 'Ronald', 'Rowan', 'Roy', 'Ryan',
                            'Sam山', 'Sammy', 'Samuel', 'Scott', 'Sean', 'Shawn', 'Sidney', 'Simon', 'Solomon', 'Spark',
                            'Spencer', 'Spike', 'Stanley', 'Steve', 'Steven', 'Stewart', 'Stuart', 'Terence', 'Terry',
                            'Ted', 'Thomas', 'Tim', 'Timothy', 'Todd', 'Tommy', 'Tom', 'Thomas', 'Tony', 'Tyler',
                            'Ultraman', 'Ulysses', 'Van', 'Vern', 'Vernon', 'Victor', 'Vincent', 'Warner', 'Warren',
                            'Wayne', 'Wesley', 'William', 'Willy', 'Zack', 'Zachary']
                random_name = random.choice( namelist )
                name = 'Jack ' + random_name
                mobile = self.cfg_test_ini.get( self.param, 'mobile' )
                appId = self.cfg_test_ini.get( self.param, 'appId' )
                channelCode = self.cfg_test_ini.get( self.param, 'channelCode' )
                # random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
                # id_card_1 = 'ALICKTEST00' + random_str
                id_card_1 = self.cfg_test_ini.get( self.param, 'mobile' )
                sql_tmp = self.cfg_sql_ini.get( 'user_id_card', 'id_card' )
                sql = sql_tmp % (name, id_card_1, mobile, appId, channelCode)
                db.update( sql, self.env_mark )
            else:
                log.error('curp_rfc校验失败！')

    def band_authBindRequest(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        mobile = data['data_checkUserExist']['mobile']
        if self.env_mark == 'nga':
            # id_card_num=str(int(time.time() * 10))
            id_card_num = self.mobile
            url_authBindRequest = data['url_authBindRequest']
            headers_authBindRequest = data['headers_authBindRequest']
            data_authBindRequest = json.dumps(data['data_authBindRequest']) % id_card_num
            res_authBindRequest = requests.post(url_authBindRequest, headers=headers_authBindRequest, data=data_authBindRequest)
            if 'Successful' in res_authBindRequest.text:
                log.info('bvn和银行卡绑卡认证通过！')
            else:
                log.error('绑卡失败！%s' % res_authBindRequest.text)
            sql_2 = self.cfg_sql_ini.get('bank_card', 'pay_bind_card') % self.user_id
            sql_3 = self.cfg_sql_ini.get('bank_card', 'user_bank_card') % self.user_id
            db.update(sql_2, self.env_mark)
            db.update(sql_3, self.env_mark)
            namelist = ['Aaron', 'Abe', 'Abelard', 'Abraham', 'Adam', 'Adrian', 'Aidan', 'Alva', 'Alex', 'Alexander',
                        'Alan', 'Eilian', 'Ailin', 'Albert', 'Alfred', 'Andrew', 'Andy', 'Angus', 'Anthony', 'Apollo',
                        'Arnold', 'Arthur', 'August', 'Austin', 'Ben', 'Benjamin', 'Bert', 'Benson', 'Bill', 'Billy',
                        'Blake', 'Bob', 'Bobby', 'Brad', 'Brandon', 'Brant', 'Brent', 'Bryan', 'Brown', 'Bruce',
                        'Caleb', 'Cameron', 'Carl',
                        'Carlos', 'Cary', 'Caspar', 'Cecil', 'Charles', 'Cheney', 'Chris', 'Christian', 'Christopher',
                        'Clark', 'Cliff', 'Cody', 'Cole', 'Colin', 'Cosmo', 'Daniel', 'Denny', 'Darwin', 'David',
                        'Dennis', 'Derek', 'Dick', 'Donald', 'Douglas', 'Duke', 'Dylan', 'Eddie', 'Edgar', 'Edison',
                        'Edmund', 'Edward', 'Edwin', 'Elijah', 'Elliott', 'Elvis', 'Eric', 'Frederick', 'Ethan',
                        'Eugene', 'Evan',
                        'Enterprise', 'Ford', 'Francis', 'Frank', 'Francis', 'Franklin', 'Fred', 'Gabriel', 'Gaby',
                        'Gabriel', 'Garfield', 'Gary', 'Gavin', 'Geoffrey', 'George', 'Gino', 'Glen', 'Glendon',
                        'Hank', 'Hardy', 'Harrison', 'Harry', 'Hayden', 'Henry', 'Hilton', 'Hugo', 'Hunk', 'Howard',
                        'Henry', 'Ian',
                        'Ignativs', 'Ignace', 'Ignatz', 'Ivan', 'Isaac', 'Isaiah', 'Jack', 'Jackson', 'Jacob', 'James',
                        'Jason', 'Jay', 'Jeffery', 'Jerome', 'Jerry', 'Gerald', 'Jeremiah', 'Jerome', 'Jesse', 'Jim',
                        'James', 'Jimmy', 'Joe', 'John', 'Johnny', 'Jonathan', 'Jordan', 'Joseph', 'Joshua', 'Justin',
                        'Keith', 'Ken', 'Kennedy', 'Kenneth', 'Kenny', 'Kevin', 'Kyle', 'Lance', 'Larry', 'Laurent',
                        'Lawrence', 'Leander', 'Lee', 'Leo', 'Leander', 'Leonard', 'Leopold', 'Leonard', 'Leopold',
                        'Leslie ', 'Loren', 'Lorry', 'Lorin', 'Louis', 'Luke', 'Marcus', 'Marcy', 'Mark', 'Marks',
                        'Mars', 'Marshal', 'Martin', 'Marvin', 'Mason', 'Matthew', 'Max', 'Michael', 'Mickey',
                        'Mike', 'Nathan', 'Nathaniel', 'Neil', 'Nelson', 'Nicholas', 'Nick', 'Noah', 'Norman', 'Oliver',
                        'Oscar', 'Owen', 'Patrick', 'Paul', 'Peter', 'Philip', 'Phoebe', 'Quentin', 'Randal',
                        'Randolph', 'Randy', 'Ray', 'Raymond', 'Reed', 'Rex', 'Richard', 'Richie', 'Rick', 'Ricky',
                        'Riley', 'Robert', 'Robin', 'Robinson', 'Rock', 'Roger', 'Ronald', 'Rowan', 'Roy', 'Ryan',
                        'Sam山', 'Sammy', 'Samuel', 'Scott', 'Sean', 'Shawn', 'Sidney', 'Simon', 'Solomon', 'Spark',
                        'Spencer', 'Spike', 'Stanley', 'Steve', 'Steven', 'Stewart', 'Stuart', 'Terence', 'Terry',
                        'Ted', 'Thomas', 'Tim', 'Timothy', 'Todd', 'Tommy', 'Tom', 'Thomas', 'Tony', 'Tyler',
                        'Ultraman', 'Ulysses', 'Van', 'Vern', 'Vernon', 'Victor', 'Vincent', 'Warner', 'Warren',
                        'Wayne', 'Wesley', 'William', 'Willy', 'Zack', 'Zachary']
            random_name = random.choice( namelist )
            name = 'Jack ' + random_name
            mobile = self.mobile
            appId = self.cfg_test_ini.get(self.param, 'appId')
            channelCode = self.cfg_test_ini.get(self.param, 'channelCode')
            sql_tmp = self.cfg_sql_ini.get('user_id_card', 'id_card')
            sql = sql_tmp % (name, mobile, appId, channelCode)
            c = db.update(sql, self.env_mark)
            # 插入代扣信息7226005439520768
            bind_card_payment_id = 'V140' + str(random.randint(0, 9999999999999999)).zfill(16)
            sql = self.cfg_sql_ini.get('bank_card', 'withholding')
            sql_1 = sql % (bind_card_payment_id, appId, self.user_id, mobile, name, id_card_num)
            db.insert(sql_1, self.env_mark)
            time.sleep(0.2)
            log.info('user更新%s条' % c)
        elif self.env_mark == 'mx':
            url_authBindRequest = data['url_authBindRequest']
            headers_authBindRequest = data['headers_bind_card']
            data_authBindRequest = json.dumps( data['data_bind_card'] )
            res_bind_card = requests.post(url_authBindRequest, headers=headers_authBindRequest, data=data_authBindRequest)
            if '0000' in res_bind_card.text:
                log.info('绑卡成功！')
            else:
                log.error('绑卡失败！%s' % res_bind_card.text)
        elif self.env_mark == 'ke':
            # 先发绑卡短信
            sendSmsCode_url = data['url_sendSmsCode']
            sendSmsCode_headers = data['headers_sendSmsCode']
            sendSmsCode_data = json.dumps( data['data_sendSmsCode_band'] )
            res_sms = requests.post( sendSmsCode_url, headers=sendSmsCode_headers, data=sendSmsCode_data )
            if '0000' in res_sms.text:
                log.info( '%s 短信发送成功！' % mobile )
            else:
                log.error( '%s 短信发送失败！' % res_sms.text )

            url_authBindRequest = data['url_authBindRequest']
            headers_authBindRequest = data['headers_bind_card']
            data_authBindRequest = json.dumps(data['band_card_date_ke'])
            res_bind_card = requests.post(url_authBindRequest, headers=headers_authBindRequest, data=data_authBindRequest)
            if '0000' in res_bind_card.text:
                log.info('绑卡成功！')
            else:
                log.error('绑卡失败！%s' % res_bind_card.text)
        elif self.env_mark == 'co':
            url_authBindRequest = data['url_authBindRequest']
            headers_authBindRequest = data['headers_bind_card']
            data_authBindRequest = json.dumps(data['band_card_date_co'])
            res_bind_card = requests.post(url_authBindRequest, headers=headers_authBindRequest, data=data_authBindRequest)
            if '0000' in res_bind_card.text:
                log.info('不绑卡成功跳过！')
            else:
                log.error('绑卡跳过失败！%s' % res_bind_card.text)
        elif self.env_mark == 'pk':
            url_authBindRequest = data['url_authBindRequest']
            headers_authBindRequest = data['headers_bind_card']
            data_authBindRequest = json.dumps( data['band_card_date_pk'] )
            res_bind_card = requests.post( url_authBindRequest, headers=headers_authBindRequest,
                                           data=data_authBindRequest )
            if '0000' in res_bind_card.text:
                log.info( '绑卡成功！' )
            else:
                log.error( '绑卡失败！%s' % res_bind_card.text )

    def apply_order(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        if self.env_mark == 'co':
            amount = 10
            data['data_createApply'].update( amount=amount )
        url_createApply = data['url_createApply']
        headers_createApply = data['headers_createApply']
        data_createApply = json.dumps(data['data_createApply'])
        res_createApply = requests.post(url_createApply, headers=headers_createApply,data=data_createApply)
        if 'Successful' in res_createApply.text:
            log.info('进件成功！执行sql将订单改为风控中……')
            time.sleep(1)
            sql1 = self.cfg_sql_ini.get('credit_order', 'loan_order_status') % self.user_id
            sql2 = self.cfg_sql_ini.get('credit_order', 'credit_order_status') % self.user_id
            a = db.update(sql1, self.env_mark)
            b = db.update(sql2, self.env_mark)
            log.info('订单表更新%s条，信审更新%s条' % (a, b))
        else:
            log.error(res_createApply.text)

    def get_order_id(self):
        time.sleep(0.3)
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_getOrderDetail = data['url_getOrderDetail']
        headers_getOrderDetail = data['headers_getOrderDetai']
        res_get_order_id = requests.get(url_getOrderDetail, headers=headers_getOrderDetail)
        loan_order_id = res_get_order_id.json()['data']['orderId']
        if 'Successful' in res_get_order_id.text:
            log.info('查询loan_order_id成功！')

        else:
            log.error('订单号：%s' % loan_order_id)
        return loan_order_id

    def credit_order_callback_pass(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_callback_order = data['url_callback_order']
        headers_callback_order = data['headers_callback_order']
        data_callback_order = json.dumps(data['data_callback_order']).replace('loan_order_id', str(self.get_order_id()))
        res_callback_order = requests.post(url_callback_order, headers=headers_callback_order, data=data_callback_order)
        if '0000' in res_callback_order.text:
            log.info("订单回调复审通过成功！")
            time.sleep(0.3)
        else:
            log.info(data + data['url_callback_order'])
            log.error("-------订单回调复审通过失败！%s" % res_callback_order.text)

    def get_admin_token(self, role_type):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        if role_type == 'dun':
            data['data_admin']['username'] = 'tanjiahua4'
            data['data_admin']['password'] = 't123456'
        elif role_type == 'admin':
            data['data_admin']['username'] = 'tanjiahua'
            data['data_admin']['password'] = '123456'
        url_admin = data['url_admin']
        headers_admin = data['headers_admin']
        data_admin = data['data_admin']
        res_get_token = requests.post(url_admin, headers=headers_admin, data=data_admin)
        token = res_get_token.json()['data']['token_type'] + ' ' + res_get_token.json()['data']['access_token']
        if '0000' in res_get_token.text:
            log.info("获取token成功！token=%s！" % token)
        else:
            log.error("获取token失败！%s！" % res_get_token.json())
        return token

    def transfer_loan(self):
        time.sleep(0.2)
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_transfer = data['url_transfer']
        headers_transfer = data['headers_transfer']
        data_transfer = data['data_transfer']
        headers_ = json.dumps(headers_transfer).replace('access_token', self.get_admin_token('admin'))
        headers = json.loads(headers_)
        data = json.dumps(data_transfer).replace('loan_order_id', self.get_order_id())
        res_transfer_loan = requests.post(url_transfer, headers=headers, data=data)
        if '0000' in res_transfer_loan.text:
            log.info("后台已触发放款成功！")
        else:
            log.error("后台已触发放款失败%s!" % res_transfer_loan.text)

    def xxl_job_login(self):
        s = requests.session()
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_job_login = data['url_job_login']
        headers_job_login = data['headers_job_login']
        data_job_login = data['data_job_login']
        res_xxl = s.post(url_job_login, headers=headers_job_login, data=data_job_login)
        if res_xxl.status_code == 200:
            log.info('xxl_job web 登录成功！')
        else:
            log.info( 'xxl_job web 登录失败！' )
        return s

    def xxl_job_execute(self):
        s = self.xxl_job_login()
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        # 放款准备
        url_job_pre = data['url_job_pre']
        headers_job_pre = data['headers_job_pre']
        data_job_pre = data['data_job_pre']
        res_xxl_pre = s.post(url_job_pre, headers=headers_job_pre, data=data_job_pre)
        if res_xxl_pre.status_code == 200:
            log.info('xxl_job 放款准备作业执行成功！')
            time.sleep(1)
        else:
            log.info( 'xxl_job 放款准备作业执行失败！' )
            time.sleep( 1 )
        loan_order_id = self.get_order_id()
        sql = self.cfg_sql_ini.get('credit_order', 'loan_order_ext') % loan_order_id
        db.update(sql, self.env_mark)
        log.info('修改放款准备完成时间成功！')

        # 完成放款
        url_job_over = data['url_job_over']
        headers_job_over = data['headers_job_over']
        data_job_over = data['data_job_over']
        res_xxl_over = s.post(url_job_over, headers=headers_job_over, data=data_job_over)
        if res_xxl_over.status_code == 200:
            log.info('xxl_job 放款完成作业执行成功！')
        else:
            log.info('xxl_job 放款完成作业执行失败！')

    def pay_notify(self):
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        if self.env_mark == 'mx':
            loan_order_id = self.get_order_id()
            url_pay = 'http://172.20.240.89:8301/v1/pandapay-notify/payoutNotify'
            sql = self.cfg_sql_ini.get('query_pay_order_id', 'pay_order_id') % loan_order_id
            data = json.dumps(
                # {"causaDevolucion": "", "empresa": "TRANSFER_TO", "estado": "Refund", "folioOrigen": "%s",
                {"causaDevolucion": "", "empresa": "TRANSFER_TO", "estado": "Success", "folioOrigen": "%s",
                 "id": "9454131"})
            try:
                result = db.query(sql, self.env_mark)
                data_pay = data % result[0]
                res_pay = requests.post(url_pay, data=data_pay)
                if res_pay.status_code == 200:
                    log.info('放款回调成功！')
                else:
                    log.info( '放款回调失败！' )
            except:
                pass
        elif self.env_mark == 'ke':
            loan_order_id = self.get_order_id()
            url_pay = 'http://172.20.240.138:8301/v1/mpesa-notify/payoutNotify'
            sql = self.cfg_sql_ini.get('query_third_trans_no', 'third_trans_no') % loan_order_id
            data = data['payoutNotify_ke']
            try:
                result = db.query(sql, self.env_mark)
                data['Result']['ConversationID'] = result[0]
                # headers={"Authorization":"Basic cm9vdDpwYXNzd29yZA=="}
                res_pay = requests.post(url_pay, data=json.dumps(data), auth=HTTPDigestAuth("root", "password"))
                if res_pay.status_code == 200:
                    log.info('放款回调成功！')
                else:
                    log.info( '放款回调失败！' )
            except:
                pass
        # elif self.env_mark == 'co':
        #     loan_order_id = self.get_order_id()
        #     url_pay = 'http://183.6.56.200:18201/pay/v1/kushki-notify/payoutNotify/cashOut'
        #     sql = self.cfg_sql_ini.get('query_third_trans_no', 'third_trans_no') % loan_order_id
        #     data = data['payoutNotify_co']
        #     try:
        #         result = db.query(sql, self.env_mark)
        #         data['ticketNumber'] = result[0]
        #         # headers={"Authorization":"Basic cm9vdDpwYXNzd29yZA=="}
        #         res_pay = requests.post(url_pay, data=json.dumps(data), auth=HTTPDigestAuth("root", "password"))
        #         if res_pay.status_code == 200:
        #             log.info('放款回调成功！')
        #         else:
        #             log.info( '放款回调失败！')
        #     except:
        #         pass

    def check_order_status(self):
        sql = self.cfg_sql_ini.get('check_order_status', 'check_order') % self.user_id
        result = list(db.query(sql, self.env_mark))
        keys = ['app', 'loan_order_id', 'mobile', 'order_status', 'loan_amount']
        check_data = dict(zip(keys, result))
        status = check_data['order_status']
        if status == 40:
            log.info('放款完成或准备成功,目前的订单状态是%s' % check_data['order_status'])
        else:
            log.error('放款完成或准备失败,目前的订单状态是%s' % check_data['order_status'])
        log.info('%s' % check_data)
        return check_data

    def synchronize_collection_job(self):
        s = self.xxl_job_login()
        res = s.post(p.url_job_over, headers=p.headers_job_over, data=p.data_job_cs)
        if res.status_code == 200:
            log.info('xxl_job 放款完成作业执行成功！')

    def syn_dun_order(self):
        date = datetime.date.today() + datetime.timedelta(days=2)
        log.info(date)
        with open( '../data/order_list.txt', 'r+', encoding='utf-8' ) as f:
            order_list = [y['loan_order_id'] for y in [eval(x) for x in f.readlines()]]
            loan_order_id = "','".join(order_list)
        sql = self.cfg_sql_ini.get('syn_dun_order', 'loan_bill_plan') % (date, "'" + loan_order_id + "'")
        log.info(sql)
        count = db.update(sql, self.env_mark)
        if count >= 1:
            log.info('应还d-2修改%s 条' % count)
        else:
            log.error('—————————— 应还d-2修改 0 条!')
        s = self.xxl_job_login()
        res_dun_d_2 = s.post(p.url_job_pre, headers=p.headers_job_pre, data=p.data_job_cs)
        if res_dun_d_2.status_code == 200:
            log.info('d-2同步催收成功！')
            time.sleep(3)
        days = 0
        date = datetime.date.today() + datetime.timedelta(days=days)
        log.info(date)
        sql1 = self.cfg_sql_ini.get('syn_dun_order', 'loan_bill_plan') % (date, "'" + loan_order_id + "'")
        sql2 = self.cfg_sql_ini.get('syn_dun_order', 'dun_loan_order') % (date, "'" + loan_order_id + "'")
        sql3 = self.cfg_sql_ini.get('syn_dun_order', 'dun_bill_plan') % (date, "'" + loan_order_id + "'")
        a1 = db.update(sql1, self.env_mark)
        a2 = db.update(sql2, self.env_mark)
        a3 = db.update(sql3, self.env_mark)
        if days < 0:
            res_dun_d_2 = s.post(p.url_job_pre, headers=p.headers_job_pre, data=p.data_job_overdue)
            if res_dun_d_2.status_code == 200:
                log.info('逾期计费job执行成功！')
        log.info(sql1)
        log.info('loan_bill_plan 更新%s条' % a1)
        log.info('dun_loan_order 更新%s条' % a2)
        log.info('dun_bill_plan 更新%s条' % a3)
        return order_list

    def assign_dun_order(self, role_type):
        order_list = self.syn_dun_order()
        loan_order_id = ",".join(order_list)
        token = self.get_admin_token(role_type)
        header_data = json.dumps(p.assign_headers).replace('access_token', token)
        headers = json.loads(header_data)
        data = json.dumps(p.assign_data).replace('loan_order_id', loan_order_id)
        res_assign_order = requests.post(p.admin_web_assign, headers=headers, data=data)
        if '0000' in res_assign_order.text:
            log.info("派单成功loan_order_id: %s！" % order_list)
        else:
            log.error("派单失败%s" % res_assign_order.text)
        return order_list

    def allow_extension(self):
        order_list = self.assign_dun_order('admin')
        headers = json.loads(json.dumps(p.assign_headers).replace('access_token', self.get_admin_token('dun')))
        for order in order_list:
            data = json.dumps(p.extension_data).replace('loan_order_id', order)
            res_allow = requests.post(p.extension_url, headers=headers, data=data)
            if '0000' in res_allow.text:
                log.info('临期展期成功！%s' % order)
            else:
                log.error('临期展期失败！')


    def get_loanBillPlanId(self):
        time.sleep(0.3)
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_loanBillPlanId = data['url_loanBillPlanId']
        headers_loanBillPlanId = data['headers_loanBillPlanId']
        headers_ = json.dumps( headers_loanBillPlanId ).replace( 'access_token', self.get_admin_token( 'admin' ) )
        headers_loanBillPlanId = json.loads( headers_ )
        data_loanBillPlanId = json.dumps(data['data_loanBillPlanId']).replace( 'loan_order_id',  self.get_order_id() )
        res_loanBillPlanId = requests.post(url_loanBillPlanId, headers=headers_loanBillPlanId,data=data_loanBillPlanId)
        loanBillPlanId = res_loanBillPlanId.json()['data']['list'][0]['loanBillPlanId']
        amount = res_loanBillPlanId.json()['data']['list'][0]['amount']
        if 'Successful' in res_loanBillPlanId.text:
            log.info('查询loanBillPlanId成功！')

        else:
            log.error('订单号：%s' % self.get_order_id())
        data_loanBillPlanId ={"loanBillPlanId":loanBillPlanId,"amount":amount}
        return data_loanBillPlanId

    def repay(self):
        time.sleep( 0.2 )
        mark = self.env_mark
        param = self.param
        data = p.loan_data.return_data( self, mark, param )
        url_repay = data['url_repay']
        headers_repay = data['headers_repay']
        data_repay = data['data_repay']
        headers_ = json.dumps( headers_repay ).replace( 'access_token', self.get_admin_token( 'admin' ) )
        headers_repay = json.loads( headers_ )
        data_repay = json.dumps( data['data_repay'] ).replace( 'loan_BillPlan_Id', self.get_loanBillPlanId()["loanBillPlanId"] )
        data_repay = data_repay.replace( 'repay_amount', self.get_loanBillPlanId()["amount"] )
        data_repay = data_repay.replace( 'loan_order_id', self.get_order_id() )
        log.info(data_repay)
        res_data_repay = requests.post( url_repay, headers=headers_repay, data=data_repay )
        if '0000' in res_data_repay.text:
            log.info( "后台已触发还款成功！" )
        else:
            log.error( "后台已触发还款失败%s!" % res_data_repay.text )

    def main_run(self, order_count,num=0):
        try:
            start_time = time.time()
            for i in range(1, int(order_count + 1)):
                # with open('mobile.txt', 'r', encoding='utf-8') as f:
                #     mobile = [x.strip('\n') for x in f.readlines()]
                # for m in mobile:
                app_name = self.cfg_test_ini.get(self.param, 'channelcode')
                # log.info('开始第【%s】次进件……' % str(mobile.index(m) + 1))
                log.info('开始第 %s【%s】次进件……' % (app_name, i))
                # self.new_mobile()
                time.sleep(0.3)
                importlib.reload(p)
                self.register()
                self.login()
                importlib.reload(p)
                # self.insert_sdk_data()
                self.submit_user_ext_contacts()
                self.create_pre_order()
                self.modify_pre_order_status()
                self.upload_image()
                time.sleep(0.2)
                self.band_authBindRequest()
                self.apply_order()
                self.credit_order_callback_pass()
                self.transfer_loan()
                self.xxl_job_execute()
                self.pay_notify()
                time.sleep(0.3)
                times = 0
                while times < 10:
                    times += 1
                    log.info('校验重试查询第{}次'.format(times))
                    time.sleep(1)
                    status = self.check_order_status()
                    if status['order_status'] == 40:
                        with open( '../data/order_list.txt', 'a+', encoding='utf-8' )as f:
                            f.write(str(status) + '\n')
                        break
                    elif status['order_status'] == 32:
                        self.xxl_job_execute()
                        time.sleep(0.5)
                    elif status['order_status'] == 35:
                        time.sleep(0.5)
                        self.pay_notify()
                    elif status['order_status'] == 36:
                        with open( '../data/order_list.txt', 'a+', encoding='utf-8' )as f:
                            f.write(str(status) + '\n')
                        break
                log.info('===========完成第【%s】次进件===========' % i)
                # log.info('===========完成第【%s】次进件===========' % str(mobile.index(m)+1))
            time_sum = time.time() - start_time
            log.info('======完成第【%s】次进件,耗时%.2fs=====' % (order_count, time_sum))
            # # log.info('======完成第【%s】次进件,耗时%.2fs=====' % (str(mobile.index(m)+1), time_sum))
            self.repay()

        except Exception as E:
            log.error(E)
            log.error(traceback.print_exc())
        finally:
            if self.env_mark == 'mx':
                pass
                # self.delete_redis_key()



if __name__ == '__main__':
    cfg_list=p.loan_data.cfg_list
    for cfg_alick in cfg_list:
        cs = BaseApi(*cfg_alick)
        cs.main_run(order_count=1)  # 新用户进件放款
    # cs.main_run()  # 新用户进件放款
    # cs.syn_dun_order()  #临期同步催收
    # cs.assign_dun_order(role_type='admin')  #临期派单
    # cs.allow_extension()         # 临期订单展期
