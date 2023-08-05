#usr/bin/env python3
#-*- coding:utf8 -*-

import queue
import threading

from urllib import parse, request
from html.parser import HTMLParser

# global constant
URLBASE = 'http://datacenter.mep.gov.cn/report/air_daily/air_dairy.jsp?city={}&startdate={}&enddate={}'
AQIKINDS = ('优', '良', '轻度污染', '中度污染', '重度污染',  '严重污染')


class URLBuilder(object):
    '''
    build url form get data
    '''
    def __init__(self, name, start_str, end_str):
        '''
        name: str, city name, chinese
        start_str: date str, 2015-05-09
        end_str: date object, 2016-01-01
        '''
        self.name = name
        self.start_str = start_str
        self.end_str = end_str

    def build(self, page=1):
        '''
        return the query url
        '''
        if page == 1:
            return URLBASE.format(parse.quote(self.name), self.start_str, self.end_str)
        return ''.join((URLBASE,'&page={}')).format(parse.quote(self.name), self.start_str, self.end_str, page)


class TrParser(HTMLParser):
    '''
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.getData = False
        self.circle_data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr' and ('height', '30') in attrs: # need notation!!!
            self.getData = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.getData = False

    def handle_data(self, data):
        if self.getData:
            self.data.append(data)

class Items(object):
    def __init__(self, text):
        self.data = []
        self.trItems = TrParser()
        self.trItems.feed(text)

    def filter(self):
        self.data = (ele for ele in self.trItems.data if '\n' not in ele)
        value = []
        # add '' after '优'
        for ele in self.data:
            value.append(ele)
            if ele == '优':
                value.append('')
        self.data = value[16:]
        self.trItems.close()

        
# 2014-12-18 is null
class TaskQueue(queue.Queue):
    def __init__(self, num_workers=1):
        queue.Queue.__init__(self)
        self.num_workers = num_workers
        self.start_workers()

    def add_task(self, task, *args, **kwargs):
        args = args or ()
        kwargs = kwargs or {}
        self.put((task, args, kwargs))

    def start_workers(self):
        for i in range(self.num_workers):
            task = threading.Thread(target=self.worker)
            task.daemon = True
            task.start()
    
    def worker(self):
        while True:
            tupl = self.get()
            item, args, kwargs = tupl
            item(*args, **kwargs)
            self.task_done()


class Crawler(object):
    def __init__(self, city_name, start_date, end_date):
        '''
        city_name: chinese name
        start_date, enddate: datetime.date() object
        '''
        self.query_builder = URLBuilder(city_name, start_date.isoformat(), end_date.isoformat())
        self.days_num = (end_date - start_date).days + 1
        self.data = None
    
    @staticmethod
    def scrapy_page(url_build, page_num, data_list, lock):
        url = url_build.build(page_num)
        html = request.urlopen(url)
        txt = html.read().decode('utf8')
        html.close()

        itms = Items(txt)
        itms.filter()

        #print("the page num is {}, the data is:".format(page_num))
        #print(itms.data)
        #print("the length of data is", len(itms.data))
        with lock:
            idx = 0
            while idx <= len(itms.data)-6:
                sample = itms.data[idx:idx+6]
                if Crawler.checkKind(sample):
                    data_list.append(tuple(sample))
                    idx += 6
                else:
                    idx += 1
        return None

    @staticmethod
    def checkKind(sample):
        '''['1', '北京市', '2015-12-28', '149', '轻度污染', 'PM2.5']
        '''
        if not sample[0].isdigit():
            return False
        date = sample[2].replace('-','')
        if not date.isdigit():
            return False
        if not sample[3].isdigit():
            return False
        if sample[4] not in AQIKINDS:
            return False
        if sample[5].isdigit():
            return False
        return True

    def scrapy(self):
        '''
        return data in the style : [('1', '北京市','2015-12-28', '14', '优', ''), ('2', '北京市','2015-12-27', '75', '良', 'PM10')]
        '''
        num = self.days_num//30 + 1
        que = TaskQueue(5)
        self.data = []
        lock = threading.Lock()
        for pg_num in range(1, num+1):
            que.add_task(Crawler.scrapy_page, self.query_builder, pg_num, self.data, lock)
        que.join()
        return None
