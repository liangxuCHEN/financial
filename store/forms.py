 #-*- coding: utf-8 -*-
from django import forms
from store.models import Item, Bill, Bill_table
from django.utils import timezone

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code', 'name', 'price']

    def clean(self):
        cleaned_data = self.cleaned_data
        code = cleaned_data.get('code')

        if Item.objects.filter(code=code).exists():
            self._errors['code'] = self.error_class(['this code exists'])  

        return cleaned_data

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
        
class AuthenticationForm(forms.Form):
            """
            Login form
            """
            username = forms.CharField(widget=forms.TextInput())
            password = forms.CharField(widget=forms.PasswordInput())

            class Meta:
                fields = ['username', 'password']