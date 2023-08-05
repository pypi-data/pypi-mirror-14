# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geokey_webresources', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='webresource',
            old_name='data_format',
            new_name='dataformat',
        ),
    ]
