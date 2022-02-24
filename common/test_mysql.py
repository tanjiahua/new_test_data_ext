# !/usr/local/Cellar/python/3.7.5/bin/python3
# -*- coding:utf-8 -*-
# Date      :2021/3/27
# FileName  :test_mysql.py
# Describe  :
# Author    :jack
import os
from configparser import RawConfigParser
from pymysql import connect as c

cfg = RawConfigParser()
path = os.path.dirname(os.path.abspath(__file__))


# 获取连接对象conn，建立数据库的连接
def get_conn(env_mark):
    if env_mark == 'mx':
        test_ini_name = 'test_ini_mx.ini'
    elif env_mark == 'nga':
        test_ini_name = 'test_ini_nga.ini'
    elif env_mark == 'ke':
        test_ini_name = 'test_ini_ke.ini'
    elif env_mark == 'co':
        test_ini_name = 'test_ini_co.ini'
    elif env_mark == 'pk':
        test_ini_name = 'test_ini_pk.ini'
    cfg.read(path + '/../config_ini/%s' % test_ini_name)
    # cfg.read(path + '/../config_ini/sql_ini_nga.ini')
    db = c(host=cfg.get('mysqld', 'ip'),
           port=int(cfg.get('mysqld', 'port')),
           user=cfg.get('mysqld', 'user'),
           passwd=cfg.get('mysqld', 'passwd'),
           db=cfg.get('mysqld', 'db_name'),
           charset='utf8',
           connect_timeout=10)
    return db


def insert(sql, env_mark):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    result = cur.execute(sql)
    conn.commit()
    cur.close()
    # conn.close()
    return result


def insert_args(sql, env_mark, args):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    result = cur.execute(sql, args)
    print(result)
    conn.commit()
    cur.close()
    conn.close()
    return result


def update_many(sql, env_mark, arg):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    result = cur.executemany(sql, arg)
    conn.commit()
    cur.close()
    # conn.close()
    return result


def update(sql, env_mark):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    result = cur.execute(sql)
    conn.commit()
    cur.close()
    # conn.close()
    return result


def query(sql, env_mark):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    # conn.close()
    return result


def delete(sql, env_mark):
    conn = get_conn(env_mark)
    cur = conn.cursor()
    result = cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return result


if __name__ == '__main__':
    cfg.read(path + '/../config_ini/sql_ini_nga.ini')
    sql = cfg.get('query_pay_order_id', 'pay_order_id') % '1395619341451792384'  # 1395619341451792384
    # sql = cfg.get('query_pay_order_id', 'pay_order_id')%'1217364434739347456' #1395619341451792384
    r = list(query(sql, 'nga'))
    print(r[0])
