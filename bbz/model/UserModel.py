# -*- coding: utf-8 -*-


from .basemodel import SafeModel
from peewee import (
    CharField,
    IntegerField
)


class UserModel(SafeModel):
    class Meta:
        # db_table 属性已经被废弃
        db_table = "user"
        table_name = "user"

    ldap_name = CharField(max_length=50, unique=True, verbose_name='ldap uid')
    user_name = CharField(max_length=50)
    emp_type = CharField(max_length=50)
    emp_number = CharField(max_length=50)
    user_mail = CharField(max_length=50)
    user_phone = CharField(max_length=20)
    department = CharField()

    @classmethod
    def query(cls, **kwargs):
        return super(cls, cls).query(cls, **kwargs)

    @classmethod
    def get_user(cls, ldap_name):
        return cls.get(cls.ldap_name == ldap_name)

    def to_dict(self):
        return self.get_field_dict()


UserModel.mapping()
