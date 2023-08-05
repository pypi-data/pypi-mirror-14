# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediastream', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediastream',
            old_name='referesh_rate',
            new_name='refresh_rate',
        ),
    ]
