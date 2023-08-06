# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_page', '0002_auto_20150707_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stackspage',
            options={'verbose_name': 'Page', 'verbose_name_plural': 'Pages', 'permissions': (('can_set_stacks_page_url', "Can edit Stacks Page 'Live URL' values"),)},
        ),
        migrations.AlterField(
            model_name='stackspage',
            name='template_path',
            field=models.CharField(default=b'stacks_page/default_page_template.html', help_text=b'The path to the template (within this django project) used to render this page. Used only by developers.', max_length=200, verbose_name='Template', choices=[('disney/disney-base.html', 'Disney Homepage')]),
        ),
    ]
