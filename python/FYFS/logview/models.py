# coding=utf-8
from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.


class UserLog(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=10)
    ip = models.GenericIPAddressField(max_length=15)
    key = models.CharField(max_length=20)
    content = models.TextField()
    created = models.DateTimeField(default=datetime.now())

    def __repr__(self):
        return "user:{},ip:{},key:{}, timesamp:{}".format(self.user, self.ip, self.key, self.created)
