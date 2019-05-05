#!/usr/bin/python3
# _*_ coding: utf-8 _*_
from datetime import datetime, timedelta


class ProxyModel(object):

    def __init__(self, data):
        self.ip = data['ip']
        port = data['port']
        self.proxy = f"https://{self.ip}:{port}"  # 设置代理https://ip:port格式

        self.blacked = False

        expire_str = data['expire_time']
        data_str, time_str = expire_str.split(' ')
        year, month, day = data_str.split('-')
        hour, minute, second = time_str.split(":")
        self.expire_time = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))

    @property
    def is_expiring(self):
        # 判断代理是否过期
        now = datetime.now()
        if (self.expire_time-now) < timedelta(seconds=5):
            return True
        else:
            return False

