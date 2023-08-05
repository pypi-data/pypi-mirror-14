# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import textplusstuff.fields
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StacksEmbed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='The name of this image.', max_length=100, verbose_name='Name')),
                ('poster_image', versatileimagefield.fields.VersatileImageField(upload_to=b'stacks_embed/poster_image', null=True, verbose_name='Poster Image', blank=True)),
                ('poster_image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', max_length=20, editable=False)),
                ('service', models.CharField(help_text=b'The service you want to embed from.', max_length=30, verbose_name='Service', choices=[(b'pbs_cove', b'COVE (PBS Video)')])),
                ('id_on_service', models.CharField(help_text=b'The ID of the content on the service.', max_length=120, verbose_name='Service ID')),
                ('embed_code', models.TextField(verbose_name='Embed Code')),
                ('optional_content', textplusstuff.fields.TextPlusStuffField(help_text='A field to enter optional accompanying content. Example uses: captions, credits or accompanying content.', verbose_name='Optional Accompanying Content', blank=True)),
                ('canonical_url', models.URLField(help_text='The originating URL of this embeddable content. Allowed domains: <p class="help">- video.pbs.org</p>', verbose_name='Canonical URL')),
                ('process_on_save', models.BooleanField(default=True, help_text=b'A boolean (True/False) signifying if this instance should be processed by its associated API on save.', verbose_name='Process on Save?')),
            ],
            options={
                'verbose_name': 'Stacks Embed',
                'verbose_name_plural': 'Stacks Embeds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksEmbedList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('list_name', models.CharField(help_text='The name of this image list.', max_length=100, verbose_name='List Name')),
            ],
            options={
                'verbose_name': 'Stacks Embed List',
                'verbose_name_plural': 'Stacks Embed Lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksEmbedListEmbed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField()),
                ('embed', models.ForeignKey(to='stacks_embed.StacksEmbed')),
                ('embed_list', models.ForeignKey(to='stacks_embed.StacksEmbedList')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stacksembedlist',
            name='embeds',
            field=models.ManyToManyField(to='stacks_embed.StacksEmbed', through='stacks_embed.StacksEmbedListEmbed'),
            preserve_default=True,
        ),
    ]
