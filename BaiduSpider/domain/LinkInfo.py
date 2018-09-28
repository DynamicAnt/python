import re


index_pattern = re.compile('http(s)?://(\w)*.cn.made-in-china.com(/)?')
prod_list_pattern = re.compile('.*/showroom/(\w)*-product-list-(\d)*.html')
prod_detail_pattern = re.compile('.*/gongying/.*')
video_pattern = re.compile('.*/video/.*')
gif_pattern = re.compile('.*/gif/.*')
tupian_pattern = re.compile('.*/tupian/.*')

qp_list_pattern = re.compile('.*(/hot-search/|-chanpin-|/cp/).*')
qc_list_pattern = re.compile('.*-gongsi-.*')
jiage_list_pattern = re.compile('.*/jiage/.*')
photo_list_pattern = re.compile('.*/photo/.*')


class Company:
    def __init__(self, com_id=0, username="none", cs_level=0, com_name="none", links=[]):
        self.com_id = com_id
        self.username = username
        self.cs_level = cs_level
        self.com_name = com_name
        self.links = links

    def append(self, link_item):
        self.links.append(link_item)

    def appends(self, arr):
        self.links.extend(arr)


class LinkItem:
    def __init__(self, url, text, ranking):
        self.url = url
        self.text = text
        self.ranking = ranking

    def console(self):
        print("ranking:%d  title:%s  url:%s " %
              (self.ranking, self.text, self.url))


class SearchResult:
    def __init__(self, word="", com_dict={}, num=0):
        self.word = word
        self.com_dict = com_dict
        self.num = num

    def append(self, attrs, link_item):
        username = attrs['data-logusername']
        if not self.com_dict.has_key(username):
            self.com_dict[username] = \
                Company(attrs['data-comid'], attrs['data-comname'], attrs['data-cslevel'], attrs['data-logusername'], [link_item])
        else:
            self.com_dict[username].append(link_item)

    def appends(self, com_dict={}):
        for username in com_dict.key():
            links = com_dict[username]
            if self.com_dict.has_key(username):
                self.com_dict[username].appends(links)
            else:
                self.com_dict[username] = links

