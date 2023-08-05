# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_embed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stacksembedlistembed',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='stacksembedlistembed',
            name='date_modified',
        ),
        migrations.AddField(
            model_name='stacksembed',
            name='display_title',
            field=models.CharField(default='Foo', help_text='The displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stacksembedlist',
            name='display_title',
            field=models.CharField(default='Foo', help_text='The displayed-to-the-user title of this content.', max_length=100, verbose_name='Display Title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stacksembedlist',
            name='name',
            field=models.CharField(default='Foo', help_text='The internal name/signifier of this content.', max_length=100, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stacksembed',
            name='canonical_url',
            field=models.URLField(help_text='The originating URL of this embeddable content. Allowed domains: <p class="help">- soundcloud.com</p><p class="help">- www.youtube.com</p><p class="help">- video.pbs.org</p><p class="help">- vimeo.com</p><p class="help">- youtu.be</p>', verbose_name='Canonical URL'),
        ),
        migrations.AlterField(
            model_name='stacksembed',
            name='name',
            field=models.CharField(help_text='The internal name/signifier of this content.', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='stacksembed',
            name='service',
            field=models.CharField(help_text=b'The service you want to embed from.', max_length=30, verbose_name='Service', choices=[(b'pbs_cove', b'COVE (PBS Video)'), (b'youtube', b'YouTube'), (b'soundcloud', b'SoundCloud'), (b'vimeo', b'Vimeo')]),
        ),
    ]
