# -*- coding: utf-8 -*-

from bbz.model.UserModel import UserModel
from bbz.model.basemodel import database


class User(object):
    def __init__(self, body):
        self.__ldap_name = body.get('ldap_name')
        self.__user_name = body.get('user_name')
        self.__emp_type = body.get('emp_type')
        self.__emp_number = body.get('emp_number')
        self.__user_mail = body.get('user_mail')
        self.__user_phone = body.get('user_phone')
        self.__department = body.get('department')

    # @database.atomic()
    @database.transaction()
    def _save(self):
        UserModel.create(
            ldap_name=self.__ldap_name,
            user_name=self.__user_name,
            emp_type=self.__emp_type,
            emp_number=self.__emp_number,
            user_mail=self.__user_mail,
            user_phone=self.__user_phone,
            department=self.__department
        )

    # @classmethod
    # def _batch_save(cls, ):
    #     UserModel.select()

    # 重写
    def __dict__(self):
        return {"ldap_name": self.__ldap_name,
                "user_name": self.__user_name,
                "emp_type": self.__emp_type,
                "emp_number": self.__emp_number
                }

    # @classmethod
    # def model2Bean(cls, *args):
    #
    #     return User("")