# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class CommentsInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    comments_id = models.CharField(max_length=100, blank=True, null=True)
    phone_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    cell = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    log_date = models.DateTimeField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_info'


class PhoneInfo(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    sell_time = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    rating_worthy_num = models.IntegerField(blank=True, null=True)
    rating_unworthy_num = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    log_date = models.DateTimeField(blank=True, null=True)
    publish_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phone_info'
