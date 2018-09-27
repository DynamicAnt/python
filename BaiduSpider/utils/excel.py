import openpyxl
import time
from db import mongodb


class ExcelUtil:
    @staticmethod
    def get_excel_row_num(filename):
        """
            获取Excel文件的行数
        :param filename: 文件名称
        """
        wb = openpyxl.load_workbook(filename=filename,read_only=True)
        ws = wb.active
        return ws.max_row

    @staticmethod
    def read_from_excel(filename, start, end):
        wb = openpyxl.load_workbook(filename=filename, read_only=True)
        ws = wb.active
        data = []
        for i in range(start, end):
            for j in range(12, 15):
                cell = ws.cell(row=i, column=j)
                if not cell.value:
                    break
                else:
                    data.append(cell.value)
        # print("关键词读取成功！")
        return data


startTime = time.clock()
## 9818
total = ExcelUtil.get_excel_row_num("2018年到期客户拆词.xlsx") + 1
db_tool = mongodb.DB()
offset = 5
start = 682
## 692
end = start + offset
while end <= total:
    db_startTime = time.clock()
    words = ExcelUtil.read_from_excel("2018年到期客户拆词.xlsx", start, end)
    db_tool.insert(words)
    print('已处理记录条数：%d' % end)
    start = end
    end = start + offset
    if end > total:
        end = total
    db_finishTime = time.clock()
    print("本次处理耗时：%f s" % (db_finishTime - db_startTime))

finishTime = time.clock()
print("共耗时%f s" % (finishTime-startTime))
# for value in word_lib:
#     print("value:" + value)
