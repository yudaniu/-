import requests
from lxml import etree
import os

base_url = 'http://www.youzi4.cc/mm/'
pj_info_url = 'http://www.youzi4.cc'
pj_url = '/index_{}.html'

# 获取分页
def get_info_page(url, pj_url, keywords):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    xhtml = etree.HTML(html)
    page_list = xhtml.xpath('//div[@class="page"]/a/text()')
    url_list = []
    if page_list:
        page_conut = page_list[-2]
        for i in range(1, int(page_conut)+1):
            p_url = pj_url.format(i)
            info_url = url + p_url
            url_list.append(info_url)
    else:
        url_list.append(url)
    for url in url_list:
        get_info_url(url, pj_info_url, keywords)

# 访问第一页并获取所有分页
def get_info_url(url, pj_url, keywords):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    xhtml = etree.HTML(html)
    pj_info_url_list = xhtml.xpath('//ul[@id="Tag_list"]/li/a/@href')
    info_url_list = []
    for i in pj_info_url_list:
        info_url = pj_url + i
        info_url_list.append(info_url)
    get_info_url_page(info_url_list, keywords)

# 访问所有分页
def get_info_url_page(info_url_list, keywords):
    page_url_list = []
    # dic_name_list = []
    for url in info_url_list:
        response = requests.get(url)
        response.encoding = 'utf-8'
        html = response.text
        xhtml = etree.HTML(html)

        # dic_name_list.append(dic_name)
        down_page = xhtml.xpath('//div[@class="page"]/a[1]/@href')
        if down_page:
            listvat = down_page[0].split('_')
            page_pj = listvat[-1].replace('2', '{}')
            info_page_url = listvat[0] + '_' + page_pj
        else:
            continue
        page_list = xhtml.xpath('//div[@class="page"]/a/text()')
        if page_list:
            page_conut = page_list[-2]
            for i in range(1, int(page_conut) + 1):
                p_url = info_page_url.format(i)
                page_url_list.append(p_url)
        else:
            continue
    for url in page_url_list:
        get_img_url(url, keywords)

# 获取图片链接
def get_img_url(url, keywords):
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    xhtml = etree.HTML(html)
    dic_name_lists = xhtml.xpath('//h1[@class="articleV4Tit"]/text()')
    dic_name = dic_name_lists[0].split('_')[0]
    img_url = xhtml.xpath('//img[@class="IMG_show"]/@src')[0]
    if img_url:
        download_image(img_url, dic_name, keywords, url)

# 下载函数
def download_image(url, dic_name, keywords, referer):
    # print(url, dic_name, keywords, referer)
    if os.path.exists(keywords+'/'+dic_name):
        pass
    else:
        os.makedirs(keywords+'/'+dic_name)
    img_name = url.split('/')[-1]
    print('正在下载'+dic_name+img_name)
    headers = {
        "Referer": referer,
    }
    res = requests.get(url, headers=headers)
    with open(keywords+'/'+dic_name+'/'+img_name, 'wb', ) as f:
        f.write(res.content)

if __name__ == '__main__':
    print('图片类型：【少妇，日本少妇，性感少妇，丝袜，黑丝，性感写真，校花】')
    keywords = input('请输入你想要爬取的类型：')
    key_list = ['少妇', '日本少妇', '性感少妇', '丝袜', '黑丝', '性感写真', '校花']
    if keywords in key_list:
        if keywords == '少妇':
            keyword = 'shaofu'
        elif keywords == '性感少妇':
            keyword = 'xingganshaofu'
        elif keywords == '日本少妇':
            keyword = 'ribenshaofu'
        elif keywords == '丝袜':
            keyword = 'siwa'
        elif keywords == '黑丝':
            keyword = 'heisi'
        elif keywords == '性感写真':
            keyword = 'xingganxiezhen'
        elif keywords == '校花':
            keyword = 'xiaohua'
    url = base_url + keyword
    get_info_page(url, pj_url, keywords)
