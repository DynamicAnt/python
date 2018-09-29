from utils import baidu
from domain import LinkInfo
from db import mongodb
import math
import queue
import threading
import contextlib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
db_tool = mongodb.DB()
word_count = db_tool.get_total_num()
analyzer = baidu.Analyzer()
spider = baidu.BaiduSpider()


def fetch(keyword):
    spider.setKeyword(keyword)
    result = LinkInfo.SearchResult(keyword)
    for i in range(0, 5):
        spider.setPageIndex(i * 10)
        content = spider.getPageContent()
        temp = analyzer.get_result(content, i * 10, 5)
        if temp.num != 0:
            result.appends(temp)
        # if not is_continue:
        #     break
    db_tool.write_to_link(result)
    # result.console()


def fetch_arr(keyword, dev=False):
    spider.setKeyword(keyword)
    result = []
    for i in range(0, 5):
        spider.setPageIndex(i * 10)
        content = spider.getPageContent()
        temp = analyzer.get_result_arr(keyword, content, i * 10, 5)
        if len(temp) != 0:
            result.extend(temp)
    if len(result) == 0:
        result.append({
            "keyword": keyword,
            "username": "",
            "com_name": "",
            "cs_level": "",
            "url": "",
            "text": "",
            "ranking": 0
        })
    if dev:
        print(str(result))
    else:
        db_tool.write_to_link(result)
    # result.console()


# 创建空对象,用于停止线程
StopEvent = object()


def callback(status, result):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :return:
    """
    pass


def action(thread_name, index):
    """
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :return:
    """
    start = index * 100 + 1
    offset = 1
    end = ((index + 1) * 100 if (index + 1) * 100 <= word_count else word_count)
    for j in range(start, end):
        words = db_tool.find_words(j, offset)
        print("index:%d keyword:%s" % (j, str(words)))
        for keyword in words:
            fetch_arr(keyword)

def log(fileName,model,msg):
    file_object = open(fileName, model, encoding='utf-8')
    file_object.write(msg+"\n")
    file_object.close()


class ThreadPool:

    def __init__(self, max_num, max_task_num=None):
        """
        初始化线程池
        :param max_num: 线程池最大线程数量
        :param max_task_num: 任务队列长度
        """
        # 如果提供了最大任务数的参数，则将队列的最大元素个数设置为这个值。
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        # 默认队列可接受无限多个的任务
        else:
            self.q = queue.Queue()
        # 设置线程池最多可实例化的线程数
        self.max_num = max_num
        # 任务取消标识
        self.cancel = False
        # 任务中断标识
        self.terminal = False
        # 已实例化的线程列表
        self.generate_list = []
        # 处于空闲状态的线程列表
        self.free_list = []

    def put(self, func, args, callback=None):
        """
        往任务队列里放入一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数
        1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        # 先判断标识，看看任务是否取消了
        if self.cancel:
            return
        # 如果没有空闲的线程，并且已创建的线程的数量小于预定义的最大线程数，则创建新线程。
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        # 构造任务参数元组，分别是调用的函数，该函数的参数，回调函数。
        w = (func, args, callback,)
        # 将任务放入队列
        self.q.put(w)

    def generate_thread(self):
        """
        创建一个线程
        """
        # 每个线程都执行call方法
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """
        循环去获取任务函数并执行任务函数。在正常情况下，每个线程都保存生存状态，
        直到获取线程终止的flag。
        """
        # 获取当前线程的名字
        current_thread = threading.currentThread().getName()
        # 将当前线程的名字加入已实例化的线程列表中
        self.generate_list.append(current_thread)
        # 从任务队列中获取一个任务
        event = self.q.get()
        # 让获取的任务不是终止线程的标识对象时
        while event != StopEvent:
            # 解析任务中封装的三个参数
            func, arguments, callback = event
            # 抓取异常，防止线程因为异常退出
            index = arguments
            try:
                # 正常执行任务函数
                result = func(current_thread, index)
                success = True
            except Exception as e:
                # 当任务执行过程中弹出异常
                result = None
                success = False
                print("任务:%d 执行失败" % index)
                print(e)
                log("error.txt", 'a', str(e) + "  关键词id：" + str(index))
            #                 self.terminate()
            # 如果有指定的回调函数
            if callback is not None:
                # 执行回调函数，并抓取异常
                try:
                    callback(success, result)
                except Exception as e:
                    pass
            # 当某个线程正常执行完一个任务时，先执行worker_state方法
            with self.worker_state(self.free_list, current_thread):
                # 如果强制关闭线程的flag开启，则传入一个StopEvent元素
                if self.terminal:
                    event = StopEvent
                # 否则获取一个正常的任务，并回调worker_state方法的yield语句
                else:
                    # 从这里开始又是一个正常的任务循环
                    event = self.q.get()
        else:
            # 一旦发现任务是个终止线程的标识元素，将线程从已创建线程列表中删除
            self.generate_list.remove(current_thread)

    def close(self):
        """
        执行完所有的任务后，让所有线程都停止的方法
        """
        # 设置flag
        self.cancel = True
        # 计算已创建线程列表中线程的个数，然后往任务队列里推送相同数量的终止线程的标识元素
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        """
        在任务执行过程中，终止线程，提前退出。
        """
        self.terminal = True
        # 强制性的停止线程
        while self.generate_list:
            self.q.put(StopEvent)

    # 该装饰器用于上下文管理
    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录空闲的线程，或从空闲列表中取出线程处理任务
        """
        # 将当前线程，添加到空闲线程列表中
        state_list.append(worker_thread)
        # 捕获异常
        try:
            # 在此等待
            yield
        finally:
            # 将线程从空闲列表中移除
            state_list.remove(worker_thread)


fetch_arr("物业用电动垃圾运输车", True)
# start = 1
# offset = 1
# while start < word_count + offset:
#     words = db_tool.find_words(start, offset)
#     print("index:%d keyword:%s" % (start, str(words)))
#     for keyword in words:
#         fetch_arr(keyword)
#     start = start + offset

# total_task = math.ceil(word_count / 100)
# pool = ThreadPool(10, total_task)
# for i in range(0, total_task):
#     pool.put(action, i, callback)



