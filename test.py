# -*- coding: utf-8 -*-

from bbz.model.UserModel import *
from bbz.model import User
import json


# import MySQLdb


def save_user():
    print("save_user...")

    user_body_1 = {
        "ldap_name": "1",
        "user_name": "",
        "emp_type": "",
        "emp_number": "",
        "user_mail": "",
        "user_phone": "",
        "department": ""
    }
    user_body_2 = {
        "ldap_name": "2",
        "user_name": "",
        "emp_type": "",
        "emp_number": "",
        "user_mail": "",
        "user_phone": "",
        "department": ""
    }

    # user = User.User(user_body_1)
    #
    # en = json.JSONEncoder.encoding
    #
    # print en(user)

    # user._save()


if __name__ == "__main__":
    uid = "zhishuai.zhou"
    # user = UserModel.query()

    # print(user.to_dict())

    user = UserModel.query(ldap_name=uid)
    # json.dumps(user)

    if user:
        user_obj = UserModel.get_user(uid)
        print(user_obj.to_dict())
        print(json.dumps(user_obj.to_dict()))
    else:
        print("no data, create")
    save_user()
