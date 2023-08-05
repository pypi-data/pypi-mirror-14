# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_embed', '0003_auto_20150528_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stacksembedlist',
            name='list_name',
        ),
    ]
