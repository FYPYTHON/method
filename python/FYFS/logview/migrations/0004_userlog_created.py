# Generated by Django 2.1.8 on 2019-10-09 05:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('logview', '0003_remove_userlog_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlog',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 9, 5, 19, 12, 331154, tzinfo=utc)),
        ),
    ]
