# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def populate_display_title(apps, schema_editor):
    """
    Populates display_title on both StacksEmbed and StacksEmbedList
    """
    StacksEmbed = apps.get_model("stacks_embed", "StacksEmbed")
    for embed in StacksEmbed.objects.all():
        embed.display_title = embed.name
        embed.save()

    StacksEmbedList = apps.get_model("stacks_embed", "StacksEmbedList")
    for embed_list in StacksEmbedList.objects.all():
        embed_list.name = embed_list.list_name
        embed_list.display_title = embed_list.list_name
        embed_list.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_embed', '0002_auto_20150528_1451'),
    ]

    operations = [
        migrations.RunPython(
            populate_display_title,
        )
    ]
