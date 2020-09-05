#使用绝对引入，后续使用import引入会忽略当前目录下的包
from __future__ import absolute_import    # 因为下面的 .celery 需要引入。  必须写在所有的 import 之前。


#如果用到 pymysql 数据库，引入下面两句：
import pymysql
pymysql.install_as_MySQLdb()


from .celery import app as celery_app   #使用了绝对引用后，.celery可以相对引入，