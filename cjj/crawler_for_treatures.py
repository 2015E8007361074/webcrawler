# coding:utf-8
"""
create on Jan 6,2017 By Wenyan Yu

由于司法商品拍卖网页的页面结构和真品拍卖网有所不同，故需要重新设计下爬虫结构

大致思路如下：

1.获取珍品拍卖日历连接 get_calendar_links() 并存储到calendar_links_treatures.csv
2.获取珍品拍卖某天的全部主题连接get_theme_links()
3.获取珍品拍卖某主题下的全部拍卖商品详细页面的连接get_detail_links()
4.获取给定时间内珍品拍卖全部拍卖商品的详细页面连接get_all_links()
5.按要求抽取商品详细页面中的信息get_page_info()

抽取的格式如下：
1.标题
2.结束时间
3.拍卖状态（已成交/流拍） 注：对于撤回和终止的拍卖商品，由于没有相关信息，对采集到页面予以舍弃，不进行抽取
4.成交价格
5.报名人数
6.提醒人数
7.围观次数
8.起拍价
9.加价幅度
10.保证金
11.佣金
12.延时周期
13.保留价
14.送拍机构
15.特色服务（没找到，默认为无）

此外获取到给定时间全部拍卖商品详细连接后，存储到links_treatures.csv
将获取到全部商品详细信息存储到page_info_treatures.csv
"""


class Crawler(object):
    """爬虫爬取拍卖网上的珍品拍卖详细信息"""
    pass



