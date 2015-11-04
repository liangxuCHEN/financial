# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    price = models.FloatField()

class Bill_table(models.Model):
    comment = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField()
    is_pay = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

class Bill(models.Model):
    item_code = models.ForeignKey(Item)
    bill_table = models.ForeignKey(Bill_table)
    bill_comment = models.CharField(max_length=200, null=True)
    number = models.IntegerField()
    created_at = models.DateTimeField()




