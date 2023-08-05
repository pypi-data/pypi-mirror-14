# install:python setup.py sdist upload
# -*- coding:utf-8 -*-
from distutils.core import setup
 
setup (
    name = 'pidan',
    version = '1.0.9.26',
    packages=["pidan"],
    platforms=['any'],
    author = 'chengang',
    author_email = 'chengang.net@gmail.com',
    description = u'更新http.get_param_from_post函数，增加三个参数类型',
    package_data = {
        '': ['*.data'],
    },
)