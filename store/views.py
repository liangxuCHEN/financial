 #-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import Item, Bill, Bill_table
from django import forms
from forms import ItemForm, BillTableForm,BillForm
from django.utils import timezone
from django.core.paginator import Paginator, InvalidPage, EmptyPage

#move to tool.py
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
# Create your views here.


def item_index(request):
    content = {}
    items = Item.objects.filter()
    content['item_list'] = items
    return render(request, 'item.html', content)

def add_one_item(request):
    """if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)"""
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
        save_mul_item(request.POST['data'])
        return HttpResponseRedirect('item')
    else:
        return render(request, 'multitem_create.html')

def bill_table_index(request):
    print '=======bill_table_index====='
    content = {}
    bill_tables = Bill_table.objects.all()

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
    print '=======add_bill_table====='
    if request.method == 'POST':
        data = request.POST
        print data
        form = BillTableForm(data)
        form.save()
        return HttpResponseRedirect('bill_table')
    else:
        print 'add_bill_table no post'
        return HttpResponseRedirect('bill_table')

def edit_bill_table(request, table_id):
    print '=======edit_bill_table====='
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
    print content["code"]
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
            #print "/bill_table_detail/%s/?info=%s" % (data['bill_table'], data['item_code']+" doesn't exsite")
            return redirect(u"/bill_table_detail/%s/?info=%s" % (data['bill_table'], data['item_code']+u" 不存在"))
            #info = data['item_code']+" doesn't exsite"
            #return redirect("/bill_table_detail/"+data['bill_table'], info=info)
    else:
        return redirect("/bill_table_detail/%s" % (data['bill_table']))

def delete_bill(request, bill_id, table_id):
    bill = Bill.objects.get(id=bill_id)
    bill.delete()
    return redirect("/bill_table_detail/"+table_id)