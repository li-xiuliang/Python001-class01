import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from snownlp import SnowNLP
import re
import datetime

class data_clean(object):
    def __init__(self):
        connect_info = 'mysql+mysqlconnector://root:123456@localhost/phonedb?charset=utf8mb4'
        self.engine = create_engine(connect_info)
        sql_phone = "SELECT * FROM phone_info;"
        sql_comments = "SELECT * FROM comments_info;"
        self.df_phone = pd.read_sql(sql=sql_phone, con = self.engine)
        self.df_comments = pd.read_sql(sql=sql_comments, con = self.engine)

    def _parse_ymd(self,s):
        s = s.split("更新时间：")[-1].strip()
        if '-' in s:
            mo,d,h,m = re.split('-| |:', s)
            return datetime.datetime(2020, int(mo), int(d), int(h), int(m))
        else:
            h, m = s.split(':')
            return datetime.datetime(datetime.date.today().year,datetime.date.today().month, datetime.date.today().day, int(h), int(m))

    def _sentiment(self,text):
        s = SnowNLP(text)
        return round(s.sentiments,2)

    def update_date(self):
        self.df_phone.dropna(how = 'any')
        self.df_comments.dropna(how = 'any')
        self.df_comments["sentiment"] = self.df_comments.content.apply(self._sentiment)
        self.df_phone['publish_time'] = self.df_phone.sell_time.apply(self._parse_ymd)
        self.df_comments.to_sql(name = 'comments_info', con = self.engine, index = False, if_exists = 'replace')
        self.df_phone.to_sql(name = 'phone_info', con = self.engine, index = False, if_exists = 'replace')

if __name__ == '__main__':
    print('start')
    data_pd = data_clean()
    data_pd.update_date()
    print('finish')


# with engine.connect() as con:
#     con.execute('alter table comments_senti chang id id int not null auto_increment;')
#engine.execute('ALTER TABLE comments_info ADD COLUMN sentiment VARCHAR(100)')