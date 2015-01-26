# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    price = models.FloatField()

class Bill(models.Model):
    item_code = models.ForeignKey(Item)
    bill_comment = models.CharField(max_length=200)
    number = models.IntegerField()
    created_at = models.DateTimeField()

class Bill_table(models.Model):
	bill_id = models.ForeignKey(Bill)
	comment = models.CharField(max_length=200)
	created_at = models.DateTimeField()
	is_pay = models.BooleanField(default=False)

	def save(self, *args, **kwaigs):
		self.created_at = timezone.now()
		super(Bill_table, self).save(*args, **kwaigs)
