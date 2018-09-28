import collections


class Company(collections.MutableMapping):
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

    def console(self):
        print("com_id:%s username:%s com_name:%s cs_level:%s" %
              (self.com_id, self.username, self.com_name, self.cs_level))
        for link in self.links:
            link.console()

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):  # 对self.data操作不会导致自身的 __contains__ 函数的递归调用
        return str(key) in self.data

    def __setitem__(self, key, item):  # 对self.data操作不会导致自身的 __setitem__ 函数的递归调用
        self.data[str(key)] = item


class LinkItem:
    def __init__(self, url, text, ranking):
        self.url = url
        self.text = text
        self.ranking = ranking

    def console(self):
        print("ranking:%d  title:%s  url:%s " %
              (self.ranking, self.text, self.url))


class SearchResult:
    def __init__(self, word=""):
        self.word = word
        self.com_dict = {}
        self.num = 0

    def append(self, attrs, link_item):
        username = attrs['data-logusername']
        if username not in self.com_dict:
            self.com_dict[username] = \
                Company(attrs['data-comid'], attrs['data-comname'], attrs['data-cslevel'], attrs['data-logusername'], [link_item])
        else:
            self.com_dict[username].append(link_item)

    def appends(self, temp):
        self.num = self.num + temp.num
        com_dict = temp.com_dict
        for username in com_dict.keys():

            if username in self.com_dict:
                links = com_dict[username].links
                self.com_dict[username].appends(links)
            else:
                self.com_dict[username] = com_dict[username]

    def console(self):
        print("关键词：%s  收录数量：%d" % (self.word, self.num))
        for username in self.com_dict.keys():
            self.com_dict[username].console()
