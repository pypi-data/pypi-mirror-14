# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_embed', '0005_auto_20150529_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='stacksembed',
            name='overline',
            field=models.CharField(help_text='An optional displayed-to-the-user overline of this content. Overlines are typically included above the Display Title.', max_length=100, verbose_name='Overline', blank=True),
        ),
    ]
