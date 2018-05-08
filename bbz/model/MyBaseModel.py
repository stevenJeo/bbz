# -*- coding: utf-8 -*-

from peewee import *

#创建数据库实例
# db = SqliteDatabase('base.db')
# db = MySQLDatabase()

#建议自己的项目使用一个新的基类，Model是peewee的基类
# class MyBaseModel(Model):
#     # class Meta:
#     #     database = db
#
#     @classmethod
#     def getOne(cls, *query, **kwargs):
#        #为了方便使用，新增此接口，查询不到返回None，而不抛出异常
#        try:
#           return cls.get(*query,**kwargs)
#        except DoesNotExist:
#            return None