# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='StacksEmbed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='The internal name/signifier of this content.', max_length=100, verbose_name='Name', blank=True)),
                ('service', models.CharField(help_text=b'The service you want to embed from.', max_length=30, verbose_name='Service', choices=[(b'pbs_cove', b'COVE (PBS Video)')])),
                ('id_on_service', models.CharField(help_text=b'The ID of the content on the service.', max_length=120, verbose_name='Service ID')),
                ('embed_code', models.TextField(verbose_name='Embed Code')),
                ('canonical_url', models.URLField(help_text='Allowed domains: - video.pbs.org', verbose_name='Embed URL')),
                ('process_on_save', models.BooleanField(default=True, help_text=b'A boolean (True/False) signifying if this instance should be processed by its associated API on save.', verbose_name='Process on Save?')),
                ('poster_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', help_text=b'NOTE: An image will be automatically generated from the URL.', null=True, verbose_name='Poster Image')),
            ],
            options={
                'verbose_name': 'Embeddable Media',
                'verbose_name_plural': 'Embeddable Media',
            },
        ),
    ]
