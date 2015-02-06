 #-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
#from django.contrib.auth import authenticate, login, logout
from store.models import Item, Bill, Bill_table
from django import forms
from store.forms import ItemForm, BillTableForm,BillForm
from django.utils import timezone
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import store.tool
import os


# Create your views here.

def item_index(request):
    content = {}
    items = Item.objects.filter()
    content['item_list'] = items
    return render(request, 'item.html', content)

def add_one_item(request):

    if request.method == 'POST':
        data = request.POST
        form = ItemForm(data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('item')
        else:
            return render(request, 'item_create.html', { "form" : form })
    else:
        form = ItemForm()
        return render(request, 'item_create.html', { "form" : form })

def add_multitems(request):
    if request.method == 'POST':
        tool.save_mul_item(request.POST['data'])
        return HttpResponseRedirect('item')
    else:
        return render(request, 'multitem_create.html')

def bill_table_index(request):
    content = {}
    bill_tables = Bill_table.objects.all()

    comment = request.GET.get('comment', '')
    if comment != '':
        bill_tables = bill_tables.filter(comment__contains=comment)
    
    has_pay = request.GET.get('has_pay','')
    if has_pay == "pay":
        bill_tables = bill_tables.filter(is_pay=True)
    if has_pay == "no_pay":
        bill_tables = bill_tables.filter(is_pay=False)

    order_date = request.GET.get('order_date','down')
    if order_date == "down":
        bill_tables = bill_tables.order_by("-created_at")
    #pages
    page_size =  10
    paginator = Paginator(bill_tables, page_size)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    
    try:
        bill_table_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bill_table_page = paginator.page(paginator.num_pages)

    content['bill_table_list'] = bill_table_page
    return render(request, 'bill_table_index.html', content)

def add_bill_table(request):
    if request.method == 'POST':
        data = request.POST
        form = BillTableForm(data)
        form.save()
        return HttpResponseRedirect('bill_table')
    else:
        return HttpResponseRedirect('bill_table')

def edit_bill_table(request, table_id):
    if request.method == 'POST':
        data = request.POST
        bill_table = Bill_table.objects.get(id=table_id)
        if data['comment']:
            bill_table.comment = data['comment']
        else:
            bill_table.comment = ""
        if 'is_pay' in data:
            bill_table.is_pay = True
        else:
            bill_table.is_pay = False
        bill_table.save()
        return redirect('/bill_table')
    else:
        return redirect('/bill_table')

def bill_table_detail(request, table_id):
    content = {}
    if 'info' in request.GET:
        content['info'] = request.GET['info']
    items = Item.objects.all()
    code = []
    for item in items:
        code.append(item.code)
    content["code"] =code
    content['bill_list'] = Bill.objects.filter(bill_table_id=table_id)
    total_price = 0
    for bill in content['bill_list']:
        total_price += bill.number * bill.item_code.price
    
    bill_table = Bill_table.objects.get(id=table_id)
    bill_table.total_price = total_price
    bill_table.save()
    content['bill_table'] = bill_table
    return render(request, 'bill_table_detail.html', content)

def add_bill(request):
    if request.method == 'POST':
        data = request.POST
        if Item.objects.filter(code=data['item_code']):
            form = BillForm(data)
            form.save()
            return redirect("/bill_table_detail/%s/?info=%s" % (data['bill_table'], u"成功添加"))
        else:
            return redirect(u"/bill_table_detail/%s/?info=%s" % (data['bill_table'], data['item_code']+u" 不存在"))
    else:
        return redirect("/bill_table_detail/%s" % (data['bill_table']))

def delete_bill(request, bill_id, table_id):
    bill = Bill.objects.get(id=bill_id)
    bill.delete()
    return redirect("/bill_table_detail/"+table_id)

def download_bill(request, table_id):
    bills = Bill.objects.filter(bill_table_id=table_id)
    data = {}
    for bill in bills:
        line = {}
        line[str(bill.id)] = {
            'id': bill.id,
            'name': bill.item_code.name,
            'code': bill.item_code.code,
            'number': bill.number,
            'price': bill.item_code.price,
            'total_price': bill.number * bill.item_code.price,
            'comment': bill.bill_comment,
        }
        data.update(line)
    
    filename = tool.create_xls(data)
    f = open(filename)
    file_data = f.read()
    f.close()
    response = HttpResponse(file_data, content_type='application/-excel')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Encoding'] = 'utf-8'
    response['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response