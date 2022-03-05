# coding=utf-8
# author= 'Jack'
# time：2022/3/5
import datetime
from pymongo import MongoClient
from configparser import RawConfigParser
from rediscluster import RedisCluster
from common import logging_func
log = logging_func.Logger().logger

def read_ini(filename):
    cfg_test_ini = RawConfigParser()
    cfg_test_ini.read('./config_ini/' + filename )
    return cfg_test_ini

def get_init_file(test_mark):
    test_mark=test_mark
    test_ini_name=""
    if test_mark == 'nga':
        test_ini_name = 'test_ini_nga.ini'
    elif test_mark == 'mx':
        test_ini_name = 'test_ini_mx.ini'
    elif test_mark == 'ke':
        test_ini_name = 'test_ini_ke.ini'
    elif test_mark == 'co':
        test_ini_name = 'test_ini_co.ini'
    elif test_mark == 'pk':
        test_ini_name = 'test_ini_pk.ini'
    cfg = RawConfigParser()
    cfg.read('./config_ini/%s' % test_ini_name)
    return cfg

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