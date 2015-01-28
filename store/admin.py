from django.contrib import admin
from store.models import Item, Bill, Bill_table

# Register your models here
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price')
    fields = ('code', 'name', 'price')

class BillTableAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'comment', 'is_pay')

admin.site.register(Item, ItemAdmin)
admin.site.register(Bill_table, BillTableAdmin)