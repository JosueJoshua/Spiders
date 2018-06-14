# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import JdItem


class CatalogSpider(scrapy.Spider):
    name = "catalog"
    allowed_domains = ["jd.com"]
    start_urls = (
        'https://dc.3.cn/category/get?&callback=getCategoryCallback&type=jsonp',
    )

    # def cate_iter(self, count, data, start):
    #     if count == 4:
    #         break
    #     s = 'catelog_%d' % count
    #     data[s] = []
    #     temp = start[i]['s']
    #     list = []
    #     for j in range(len(temp)):
    #         content = temp[j]['n'].split('|')[1].encode('utf-8')
    #         list.append(content)
    #         if j == len(temp) - 1:
    #             data[s].append(list)
    #             print json.dumps(data[s], ensure_ascii=False)
    #         cate_iter(count + 1, data, temp)

    def parse(self, response):
        catalog_data = JdItem()
        data_json = response.body.decode('gbk')
        data = json.loads(data_json[20:-1])
        data_ZN = json.dumps(data, ensure_ascii=False)
        s = data['data']
        print len(s)
        catalog_data['first_cat'] = []
        catalog_data['second_cat_channel'] = []
        catalog_data['second_cat'] = []
        catalog_data['three_cat'] = []
        list_temp = []

        for i in range(len(s)):
            s1 = data['data'][i]['s']  # 一级获取位置
            list1 = []
            for j in range(len(s1)):
                content = s1[j]['n'].split('|')[1].encode('utf-8')  # 一级目录单项内容
                list1.append(content)

                s_cat = s1[0]['s']  # 二级获取位置
                list3 = []
                for k in range(len(s_cat)):
                    #print k
                    content = s_cat[k]['n'].split('|')[1].encode('utf-8')  # 二级目录单项内容
                    list3.append(content)

                    list4 = []
                    for l in range(len(s_cat[k]['s'])):
                        content = s_cat[k]['s'][l]['n'].split('|')[1].encode('utf-8')  # 三级目录单项内容
                        list4.append(content)
                    catalog_data['three_cat'].append(list4)  # 三级目录
                catalog_data['second_cat'].append(list3)  # 二级目录
            catalog_data['first_cat'].append(list1)  # 一级目录


            s2 = data['data'][i]['t']  # 二级通道获取位置
            list2 = []
            for j in range(len(s2)):
                content = s2[j].split('|')[1].encode('utf-8')  # 二级通道单项内容
                list2.append(content)
            catalog_data['second_cat_channel'].append(list2)  # 二级通道

            #print catalog_data['first_cat']
            #print json.dumps(list1, ensure_ascii=False)
        print json.dumps(catalog_data['first_cat'], ensure_ascii=False)
        print json.dumps(catalog_data['second_cat_channel'], ensure_ascii=False)
        print json.dumps(catalog_data['second_cat'], ensure_ascii=False)
        print json.dumps(catalog_data['three_cat'], ensure_ascii=False)
        return catalog_data
