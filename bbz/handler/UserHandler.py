# -*- coding: utf-8 -*-

import json
from BaseHandler import BaseHandler
from BaseHandler import json_response
from BaseHandler import JsonResponse
from bbz.model.User import *
from webargs.tornadoparser import use_args
from marshmallow import fields


class QueryUserHandler(BaseHandler):
    """
        查询处理器
    """
    update_args = {
        '''提交的是表单？？？？'''
        "action": fields.Int(required=False),
        "result": fields.List(fields.Dict(required=True), required=True)
    }

    @json_response()
    @use_args(update_args)
    def post(self, args):

        action = args.get("action")

        # name = self.request.body.get("name", "")
        # user_name = self.get_current_user()

        cookies = {
            "user_name": self.get_cookie('user_name'),
            "username": self.get_cookie('username'),
            "operator_sign": self.get_cookie('operator_sign'),
            "operator_ticket": self.get_cookie('operator_ticket'),
            "operator_timestamp": self.get_cookie('operator_timestamp')
        }
        print("cookies=", cookies)
        operator = self.get_current_user()

        uuuu = self.get_cookie("user_name")
        nnnnn = self.get_secure_cookie("user_name")

        self.get_secure_cookie_key_version()

        Q = True
        if self.request.body.get("name"):
            Q &= UserModel.ldap_name.contains(self.request.body.get("name", ""))
        if self.request.body.get("emp_number"):
            Q &= UserModel.ldap_name.contains(self.request.body.get("emp_number", ""))
        if self.request.body.get("emp_type"):
            Q &= UserModel.emp_type == self.request.body.get("emp_type", "")

        users = (UserModel.select()).where(Q)
        count = users.count()

        response = []
        for u in users.dicts():
            response.append(self.transition(u))

        return response

    def get(self):
        print("get_user_")
        self.write("hello steven")


class UpdateUserHandler(BaseHandler):
    """
    更新处理器
    """

    def post(self, *args, **kwargs):
        pass


class SaveUserHandler(BaseHandler):
    """
    保存处理器
    """

    @json_response()
    def post(self, *args, **kwargs):
        param = self.transition(self.request.body)
        name = param.get("name")
        ladp_name = param.get("ladp_name")

        save_body = {
            "ldap_name": param.get("ladp_name"),
            "user_name": param.get("name")
        }

        user = User(save_body)
        user._save()

        return {"data": "保存成功"}
