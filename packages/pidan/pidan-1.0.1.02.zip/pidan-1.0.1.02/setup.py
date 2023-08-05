# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.1.02',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'增加中国人姓名验证函数',
    package_data = {
        '': ['*.data'],
    },
)