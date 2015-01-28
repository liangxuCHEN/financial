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
