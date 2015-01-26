from django.contrib import admin
from store.models import Item, Bill, Bill_table
# Register your models here.
admin.site.register(Item)
admin.site.register(Bill)
admin.site.register(Bill_table)