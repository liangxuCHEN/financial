from django import forms
from models import Item, Bill, Bill_table

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['code', 'name', 'price']

class MultitemForm(forms.ModelForm):
	data = forms.CharField(widget=forms.Textarea)