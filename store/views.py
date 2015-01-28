from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import Item, Bill, Bill_table
from django import forms
from forms import ItemForm, BillTableForm


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
