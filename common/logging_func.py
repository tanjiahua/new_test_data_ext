# !/usr/local/Cellar/python/3.7.5/bin/python3
# -*- coding:utf-8 -*-
# Date      :2021/3/27
# FileName  :logging.py
# Describe  :
# Author    :jack

from datetime import datetime
import os
from configparser import ConfigParser
import logging
from logging import handlers

cfg = ConfigParser()
path = os.path.dirname(os.path.abspath(__file__))
cfg.read(path + '/../config_ini/logconfig.ini')
log_file = path + '/../' + '/log_file/app%s.log' % datetime.now().strftime('%Y%m%d%H%M%S')


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL}

    def __init__(self, filename=log_file, level='info', when='D', backCount=3,
                 fmt=cfg.get('formatter_defaultFormatter', 'format', raw=True)):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,encoding='utf-8')
        th.setFormatter(format_str)
        if not self.logger.handlers:
            self.logger.addHandler(sh)
            self.logger.addHandler(th)


# if __name__ == '__main__':
#     log = Logger(log_file, level='debug')
#     log.logger.debug('debug')
#     log.logger.info('info')
#     log.logger.warning('警告')
#     log.logger.error('报错')
#     log.logger.critical('严重')
#     Logger('error.log', level='error').logger.error('error')
