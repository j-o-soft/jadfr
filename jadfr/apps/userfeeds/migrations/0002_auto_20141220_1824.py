# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userfeeds', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfeedentry',
            unique_together=set([('feed', 'entry')]),
        ),
    ]
