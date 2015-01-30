from django import forms
from models import Item, Bill, Bill_table
from django.utils import timezone

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code', 'name', 'price']

class BillTableForm(forms.ModelForm):
    class Meta:
        model = Bill_table

    def save(self): # create new table
        new_table=Bill_table.objects.create(
            created_at=timezone.now(),
            total_price=0,
            comment=self.data['comment'],
        )

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill

    def save(self): # create new bill
        new_table=Bill.objects.create(
            item_code=Item.objects.get(code=self.data['item_code']),
            bill_table=Bill_table.objects.get(id=self.data['bill_table']),
            created_at=timezone.now(),
            number=self.data['number'],
            bill_comment=self.data['bill_comment'],
        )