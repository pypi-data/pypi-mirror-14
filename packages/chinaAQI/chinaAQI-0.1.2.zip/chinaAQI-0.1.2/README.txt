#coding:utf8
Description:
    The chinaAQI means china city Air Quality Index which is announced by china government
    everday since 1st.Jan.2014.
    Each row contains six elements:
        (1.number 2.city name 3.date       4.air quality index 5.air quality degree 6.primary pollutan)
        '1',       '北京市',  '2015-12-28', '149',                 '轻度污染',          'PM2.5'
How to use:
    Python version: 3.0 or above
    pip install chinaAQI
    import datetime
    import chinaAQI
    city = '北京市'
    start = datetime.date(2015,1,1)
    end = datetime.date(2016,1,1)
    crawler = chinaAQI.Crawler(city, start, end)
    crawler.scrapy()
    print(crawler.data)
Conntact me:
    ludlows@foxmail.com
    https://github.com/ludlows/chinaAQI
