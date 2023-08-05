# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def pbs_cove_allowfullscreen(apps, schema_editor):
    """
    Updates all existing all PBS COVE partner play embed codes to include
    'allowfullscreen'.
    """
    StacksEmbed = apps.get_model("wagtail_stacks_embed", "StacksEmbed")
    for embed in StacksEmbed.objects.filter(service='pbs_cove'):
        embed_code = embed.embed_code.replace(
            "'></iframe>",
            "' allowfullscreen></iframe>"
        )
        embed.embed_code = embed_code
        embed.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_stacks_embed', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(pbs_cove_allowfullscreen)
    ]
