from django.contrib import admin
from store.models import Item, Bill, Bill_table

# Register your models here
class ItemAdmin(admin.ModelAdmin):
	fields = ('code', 'name', 'price')
admin.site.register(Item, ItemAdmin)
admin.site.register(Bill)
admin.site.register(Bill_table)