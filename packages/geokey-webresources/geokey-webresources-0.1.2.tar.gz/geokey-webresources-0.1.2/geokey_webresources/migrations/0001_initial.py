# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0007_auto_20160122_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[(b'active', b'active'), (b'inactive', b'inactive'), (b'deleted', b'deleted')], default=b'active', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('data_format', models.CharField(choices=[(b'GeoJSON', b'GeoJSON'), (b'KML', b'KML'), (b'GPX', b'GPX')], max_length=10)),
                ('url', models.URLField(max_length=250)),
                ('order', models.IntegerField(default=0)),
                ('colour', models.TextField(default=b'#0033ff')),
                ('symbol', models.ImageField(blank=True, max_length=500, null=True, upload_to=b'webresources/symbols')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webresources', to='projects.Project')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
