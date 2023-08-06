# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stackspage',
            name='keywords',
            field=models.CharField(help_text=b"Used to populate the 'Keywords' meta tag (used for SEO).", max_length=300, verbose_name='Keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='stackspage',
            name='description',
            field=models.TextField(help_text=b'A short description of the page. The text entered here will be used for SEO and Facebook share text.', verbose_name='Page Description'),
        ),
        migrations.AlterField(
            model_name='stackspage',
            name='publish',
            field=models.BooleanField(default=False, help_text=b'Signifies whether this page is viewable to the public.', verbose_name='Publish Live on Save?'),
        ),
    ]
