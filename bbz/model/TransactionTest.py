#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 上午11:36

from bbz.model.UserModel import UserModel
from bbz.model.basemodel import database


class TransactionModel(object):
    """
    事务的相关操作
    """

    def __init__(self, body):
        self.__name = body.get("name")
        self.__age = body.get("age")
        self.__address = body.get("address")

    @database.atomic()
    def save_atomic(self):
        """
        使用装饰器自动管理, 有异常自动回滚
        :return:
        """
        return UserModel.insert()

    def save_manual(self):
        """
        纯手动提交，异常手动回滚
        :return:
        """
        with database.transaction() as tx:
            try :
                """ DB操作 """
                row = UserModel.insert()
                tx.commit()
            except Exception as ex:
                tx.rollback()
            return row

    def save_half_atomic(self, **body):
        """
        半自动用savepoint上下文管理
        :return:
        """
        with database.transaction() as tx:
            with database.savepoint() as sp1:
                row_1 = UserModel.insert(body.get("body_1"))

            with database.savepoint() as sp2:
                row_2 = UserModel.insert(body.get("body_2"))
                sp2.rollback()
                # "body_2" will not be saved, but "body_1" will be saved.

            tx.commit()
