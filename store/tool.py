 #-*- coding: utf-8 -*-
from models import Item
from xlwt import Workbook
import datetime

def save_mul_item(text):
    text=text.replace('\r\n', '')
    items = text.split(";")
    for item in items:
        content = item.split(" ")
        if len(content) == 3:
            #is unique ?
            try:
                Item.objects.create(
                    code=content[0],
                    name=content[1],
                    price=float(content[2])
                )
            except Exception as e:
                print e

def create_xls(data):
    work = Workbook(encoding='utf-8')
    work_sheet = work.add_sheet(u'账单')
    #head of table    
    work_sheet.write(0, 0, 'ID')
    work_sheet.write(0, 1, u'名字')
    work_sheet.write(0, 2, u'编码')
    work_sheet.write(0, 3, u'数量')
    work_sheet.write(0, 4, u'单价')
    work_sheet.write(0, 5, u'合计')
    work_sheet.write(0, 6, u'备注')
    i = 1
    total_price = 0
    for row in data:
        work_sheet.write(i, 0, str(i))
        work_sheet.write(i, 1, data[row]['name'])
        work_sheet.write(i, 2, data[row]['code'])
        work_sheet.write(i, 3, data[row]['number'])
        work_sheet.write(i, 4, data[row]['price'])
        work_sheet.write(i, 5, data[row]['total_price'])
        work_sheet.write(i, 6, data[row]['comment'])
        total_price += data[row]['number'] * data[row]['price']
        i = i + 1
    work_sheet.write(i, 4, u'总价:')
    work_sheet.write(i, 5, total_price)
    time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "download_xls/bill_%s.xls" % time_stamp
    work.save(file_name)
    return file_name
    #download_file(file_name)
