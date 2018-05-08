# -*- coding: utf-8 -*-

import json
import jsonschema
import decimal
from tornado.web import RequestHandler
from webargs.tornadoparser import use_args
from marshmallow import fields
from functools import wraps
from bbz.utils.log import log_info
from bbz.utils.log import log_stdout


class BaseHandler(RequestHandler):

    @use_args({"user_name": fields.Str(required=True, location='cookies')})
    def get_current_user(self, args):
        return args.get('user_name', "")

    @property
    def db(self):
        return self.application.db

    def transition(self, data):
        import datetime

        def loop(message):
            if isinstance(message, list):
                for index, msg in enumerate(message):
                    message[index] = loop(msg)
            if isinstance(message, dict):
                for key, value in message.items():
                    message[key] = loop(value)
            if isinstance(message, unicode):
                message = message.encode("utf-8").strip()
            elif isinstance(message, float):
                message = str(int(message))
            elif isinstance(message, datetime.date):
                message = str(message)
                if message == "9999-12-31":
                    message = ""
            elif isinstance(message, decimal.Decimal):
                message = float(message)
            elif not message:
                if isinstance(message, list):
                    message = []
                elif isinstance(message, dict):
                    message = {}
                else:
                    message = ""
            return message

        return loop(data)


class JsonResponse(object):

    def __call__(self, func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            output = dict(status=0, msg="success", data=None)
            try:
                ret = func(*args, **kwargs)
                if not ret:
                    if isinstance(ret, list):
                        output['data'] = []
                    else:
                        output['data'] = {}
                # if isinstance(ret, dict) and 'data' in ret:
                #     output['data'].update(ret)
                else:
                    output['data'] = ret
            except ServerErr as ex:
                output['status'] = ex.errcode
                output['msg'] = ex.message
            except Exception as ex:
                output['status'] = -1
                output['msg'] = str(ex)
            finally:
                try:
                    print 'output:{}'.format(output)
                    print json.dumps(output)
                    args[0].set_header('Access-Control-Allow-Origin', '*')
                    args[0].write(json.dumps(output))
                    if output['status'] != 0:
                        level = "error"
                    else:
                        level = "info"
                    log_info.info(log_stdout(
                        level=level,
                        method="{}.{}".format(args, func.__name__),
                        Output=output,
                        Input=kwargs,
                        description=""
                    ))
                except Exception as ex:
                    pass
                args[0].finish()

        return _wraps


def json_response(request_body_schema=None):
    """检测 GET、POST 请求的参数形式
    :param dict request_body_schema: schema 语法
    :rtype json
    """

    def add_schema(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # func(*args, **kwargs)
            # 设定返回 JSON 的默认格式
            response = dict(status=0, data={}, msg="success")

            # 获取本地 request 的请求方法
            method = args[0].request.__dict__.get("method")
            if method == "GET":
                # GET 方法需要从 self.request.query_arguments 讲参数转换为 map 形式
                body = args[0].request.query_arguments
                for key, value in body.iteritems():
                    body[key] = value[0]
            elif method == "POST":
                # POST 方法直接从 self.request.body 中获取 body
                if not args[0].request.files:
                    try:
                        body = json.loads(args[0].request.body)
                        args[0].request.body = body
                    except Exception:
                        response["status"] = -1
                        response["msg"] = "the json format is invalid!"
                        args[0].write(json.dumps(response))
                else:
                    body = args[0].request.body

            # func(*args, **kwargs)
            try:
                if request_body_schema:
                    try:
                        jsonschema.validate(body, request_body_schema)
                    except jsonschema.ValidationError:
                        raise jsonschema.ValidationError("parameter format validation failed!")

                result = func(*args, **kwargs)

                if isinstance(result, dict):
                    response["data"].update(result)

                if isinstance(result, list):
                    response["data"] = result

            except Exception as e:
                response["status"] = -1
                response["msg"] = str(e)
            finally:
                args[0].write(json.dumps(response))

        print("wrapper")
        return wrapper

    print("add_schema")
    return add_schema


class ServerErr(Exception):

    def __init__(self, errcode, message):
        self.errcode = errcode
        self.message = message

    def __str__(self):
        return '[Server Error] {}, error code {}'.format(self.message, self.errcode)
