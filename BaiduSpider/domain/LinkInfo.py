
class LinkItem:
    def __init__(self, url, text, username, ranking=0):
        self.url = url
        self.text = text
        self.username = username
        self.ranking = ranking

    def console(self):
        print("title:%s  url:%s  username:%s ranking:%d" % (self.text, self.url, self.username, self.ranking))


class SearchResult:
    def __init__(self, word=""):
        self.word = word
        self.links = []

    def append(self, link_item):
        self.links.append(link_item)

    def appends(self, arr):
        self.links.extend(arr)
