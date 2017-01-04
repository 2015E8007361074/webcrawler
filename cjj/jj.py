import requests


def get_first_id():
    header = {':authority': 'paimai.taobao.com',
    ':method': 'GET',
    ':path': '/ json / pmp_notice.htm?_input_charset = utf - 8 & date = 2016 - 11 - 10 & day = 10 & page = 1 & cat = 53904005 % 2 C53920002 % 2 C53872005 % 2C53950002 & city = & _ksTS = 1481897831661_1829 & callback = jsonp1830',
    ':scheme':'https',
    'accept': 'text / javascript, application / javascript, application / ecmascript, application / x - ecmascript, * / *; q = 0.01',
    'accept - encoding': 'gzip, deflate, sdch, br',
    'accept - language': 'en - US, en; q = 0.8',
    'content - type': 'application / x - www - form - urlencoded; charset = UTF - 8',
    'cookie': 'thw=cn; cna=kc+NEPrJITwCAW/ITWcuqYN/; v=0; cookie2=1cb34b906771c3217bbdd4cd3815de6d; t=c84f4d32afc82239f2343522fda5cf5f; _tb_token_=2JYbNc0Bq; CNZZDATA1253345903=1551481119-1481895066-%7C1481895066; mt=ci%3D-1_0; uc1=cookie14=UoW%2FXGduASeM8w%3D%3D; l=AoeH4AKlaZjdT41Uw/FLFdqflzFW0l/K; isg=AhMTT-f3T2mm6wMsjYNw4fF4opHQsi94o5ph68U3MTbNRDjmTZgr2ltSGAPQ',
    'referer':'https://paimai.taobao.com/calendar.htm?spm=a2129.3065125.0.0.y9CcFX',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    'x-requested-with':'XMLHttpRequest'
    }

    r = requests.get('https://paimai.taobao.com/json/pmp_notice.htm?_input_charset=utf-8&date=2016-11-10&day=10&page=2&cat=53904005%2C53920002%2C53872005%2C53950002&city=&_ksTS=1481897831661_1829&callback=jsonp1830',
                      headers =header, timeout=5,)

    print (r.text)


def get_page():
    r = requests.get('https://item-paimai.taobao.com/pmp_item/537655013805.htm?s=pmp_detail', timeout=5,)
    print (r.text)

get_page()
