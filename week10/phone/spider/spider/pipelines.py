# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from scrapy.utils.project import get_project_settings
import uuid

Base = declarative_base()
settings = get_project_settings()

class PhoneInfo(Base):
    __tablename__ = 'phone_info'
    id = Column(String(100), primary_key = True)
    name = Column(String(200), comment = '手机名称')
    price = Column(Integer(), comment = '手机价格')
    sell_time = Column(String(100), comment = '发布时间')
    author = Column(String(100), comment = '本文作者')
    rating_worthy_num = Column(Integer(), comment = '打分：值')
    rating_unworthy_num = Column(Integer(), comment = '打分：不值')
    description = Column(String(2000), comment = '描述信息')
    log_date = Column(DateTime(), default = datetime.now, onupdate = datetime.now, comment = '记录日期')

class CommentsInfo(Base):
    __tablename__ = 'comments_info'

    def gen_id(self):
        return uuid.uuid4().hex

    id = Column(String(100), primary_key = True, default = gen_id)
    comments_id = Column(String(100), comment = '评论者ID')
    phone_id = Column(String(100), comment = '手机ID')
    name = Column(String(200), comment = '评论作者')
    cell = Column(String(20), comment = '评论楼层')
    content = Column(String(2000), comment = '评论内容')
    log_date = Column(DateTime(), default = datetime.now, onupdate = datetime.now, comment = '记录日期')

class SpiderPipeline(object):
    def __init__(self):
        conntion = settings['MYSQL_CONNECTION']
        engine = create_engine(conntion, echo = False)
        DBSession = sessionmaker(bind = engine)
        self.SQLsession = DBSession()
        try:
            Base.metadata.drop_all(engine)
        except:
            pass
        Base.metadata.create_all(engine)

    def phone_db(self, info):
        id = info['id']
        temp = self.SQLsession.query(PhoneInfo).filter_by(id = id).first()
        if temp:
            temp.name = info.get('name', '')
            temp.price = info.get('price', '')
            temp.sell_time = info.get('sell_time', '')
            temp.author = info.get('author', '')
            temp.rating_worthy_num = info.get('rating_worthy_num', '')
            temp.rating_unworthy_num = info.get('rating_unworthy_num', '')
            temp.description = info.get('description', '')
        else:
            inset_data = PhoneInfo(
                id = info.get('id', ''),
                name = info.get('name', ''),
                price = info.get('price', ''),
                sell_time = info.get('sell_time', ''),
                author = info.get('author', ''),
                rating_worthy_num = info.get('rating_worthy_num', ''),
                rating_unworthy_num = info.get('rating_unworthy_num', ''),
                description = info.get('description', ''),
            )
            self.SQLsession.add(inset_data)
        self.SQLsession.commit()

    def comments_db(self, info):
        comments_id = info['comments_id']
        cell = info['cell']
        phone_id = info['phone_id']
        temp = self.SQLsession.query(CommentsInfo).filter_by(comments_id = comments_id).filter_by(cell = cell).filter_by(phone_id = phone_id).first()
        if temp:
            temp.name = info.get('name', '')
            temp.content = info.get('content', '')
        else:
            inset_data = CommentsInfo(
                comments_id = info.get('comments_id', ''),
                cell = info.get('cell', ''),
                phone_id = info.get('phone_id', ''),
                name = info.get('name', ''),
                content = info.get('content', ''),
            )
            self.SQLsession.add(inset_data)
        self.SQLsession.commit()

    def process_item(self, item, spider):
        self.phone_db(item['phone_info'])
        self.comments_db(item['comments_info'])
        return item
