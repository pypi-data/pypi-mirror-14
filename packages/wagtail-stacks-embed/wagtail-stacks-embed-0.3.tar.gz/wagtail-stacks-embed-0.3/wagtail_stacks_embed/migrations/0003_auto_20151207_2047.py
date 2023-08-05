# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_stacks_embed', '0002_auto_20151002_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stacksembed',
            options={'ordering': ('-date_created', '-date_modified'), 'verbose_name': 'Embeddable Media', 'verbose_name_plural': 'Embeddable Media'},
        ),
        migrations.AlterField(
            model_name='stacksembed',
            name='canonical_url',
            field=models.URLField(help_text='Allowed domains: soundcloud.com www.youtube.com video.pbs.org vimeo.com youtu.be', verbose_name='Embed URL'),
        ),
        migrations.AlterField(
            model_name='stacksembed',
            name='service',
            field=models.CharField(help_text=b'The service you want to embed from.', max_length=30, verbose_name='Service', choices=[(b'pbs_cove', b'COVE (PBS Video)'), (b'youtube', b'YouTube'), (b'soundcloud', b'SoundCloud'), (b'vimeo', b'Vimeo')]),
        ),
    ]
