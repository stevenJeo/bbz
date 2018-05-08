# -*- coding: utf-8 -*-

from peewee import (
    MySQLDatabase,
    Model,
    ForeignKeyField
)

from time import sleep
from datetime import datetime


class SafeMySQLDatabase(MySQLDatabase):

    def get_conn(self):
        try_count = 10
        _conn = None
        while try_count > 0:
            try:
                _conn = super(SafeMySQLDatabase, self).get_conn()
                _curs = _conn.cursor()
                _curs.execute("select 1")
                _curs.close()
                break
            except Exception as ex:
                # log_info.info("数据库连接error:{}".format(ex))
                print("数据库连接error:{}", ex)
                try:
                    self.close()
                except:
                    # log_info.info('mysql close() failed, {}'.format(ex))
                    print("mysql close() failed, {}", ex)
                    pass
                sleep(1)
            try_count -= 1
        if _conn is None:
            raise Exception('mysql can\'t connect')
        return _conn


# database = demo_new
# password = 096667f9c7d0396d
# port     = 33009
# user     = dev
# host     = 10.255.206.179
# charset  = utf8

database = SafeMySQLDatabase(
    database="demo_new",
    passwd="123456",
    port=3306,
    user="root",
    host="localhost",
    charset="utf8"
)


class SafeModel(Model):
    class Meta:
        database = database

    def get_field_dict(self):
        field_dict = {}

        for field in self._meta.fields.values():
            if isinstance(field, ForeignKeyField):
                field_dict[field.name] = getattr(self, field.id_storage)
            else:
                field_dict[field.name] = getattr(self, field.name)
            if field_dict[field.name] is None:
                field_dict.pop(field.name)
            if isinstance(field_dict[field.name], datetime):
                field_dict[field.name] = field_dict[field.name].strftime('%Y-%m-%d %H:%M:%S')
        return field_dict

    @classmethod
    def mapping(cls):
        if not cls.table_exists():
            print("table not exist....")
            cls.create_table()

    @classmethod
    def query(cls, subclass, order_by=True, **kwargs):
        """查询对应表中所有的数据

        :param object subclass: 继承 Model 类的子类对象
        :param bool order_by:
            - True  升序
            - False 降序
        """
        # 将所有查询提供的参数增加至 condition map 中
        condition = {}
        for name in subclass()._meta.fields.keys():
            if name == "pid" and kwargs.get("pid") == 0:
                condition[name] = 0
            if kwargs.get(name):
                condition[name] = kwargs.get(name)

        # 拼接 condition 中的条件查询语句
        Q = True
        for key in condition:
            if isinstance(condition.get(key), list) and condition.get(key):
                Q &= (getattr(subclass, key).in_(condition.get(key)))
            else:
                Q &= (getattr(subclass, key) == condition.get(key))

        # 如果没有查询条件获取所有数据
        if isinstance(Q, bool):
            R = subclass.select()
        else:
            R = subclass.select().where(Q)

        # 排序方案
        if order_by:
            R = R.order_by(subclass.id)
        else:
            R = R.order_by(subclass.id.desc())

        # 分页配置
        if kwargs.get("page_no") and kwargs.get("page_size"):
            R = R.paginate(kwargs.get("page_no"), kwargs.get("page_size"))

        print("R=", R.order_by)
        return R
