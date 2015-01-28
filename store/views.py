from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import Item, Bill, Bill_table
from django import forms
from forms import ItemForm, BillTableForm,BillForm
from django.utils import timezone


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
    content = {}
    bill_tables = Bill_table.objects.filter()
    content['bill_table_list'] = bill_tables
    return render(request, 'bill_table_index.html', content)

def add_bill_table(request):
    if request.method == 'POST':
        data = request.POST
        print data
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
            bill_table.save()
        return redirect('/bill_table')
    else:
        return redirect('/bill_table')

def bill_table_detail(request, table_id):
    content = {}
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
        print data
        form = BillForm(data)
        form.save()
        return redirect("/bill_table_detail/"+data['bill_table'])
    else:
        return redirect("/bill_table_detail/"+data['bill_table'])