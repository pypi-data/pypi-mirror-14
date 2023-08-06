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
            name='StacksPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text=b'The title of the page. Currently only used for SEO.', max_length=100, verbose_name='Page Title')),
                ('slug', models.SlugField(unique=True, verbose_name='Page Slug')),
                ('description', models.TextField(help_text=b'A short description of the page. Currently only used for SEO.', verbose_name='Page Description')),
                ('twitter_share_text', models.CharField(help_text=b'The text to use when sharing this page to Twitter. Limited to 110 characters.', max_length=110, verbose_name='Twitter Share Text', blank=True)),
                ('canonical_image', versatileimagefield.fields.VersatileImageField(help_text=b'An image that represents this page. Is used when this page is shared on social media.', upload_to=b'images/canonical', max_length=300, verbose_name='Canonical Image', blank=True)),
                ('canonical_image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', max_length=20)),
                ('publish', models.BooleanField(default=False, help_text=b'Signifies whether this page is viewable to the public.', verbose_name='Publish Live?')),
                ('template_path', models.CharField(default=b'stacks_page/default_page_template.html', help_text=b'The path to the template (within this django project) used to render this page. Used only by developers.', max_length=200)),
                ('live_url', models.URLField(help_text=b'The URL this page will live at once live in production.', max_length=250, verbose_name='Live URL', blank=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StacksPageSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('title_section', models.CharField(help_text=b'The title of this section.', max_length=140, verbose_name='Title')),
                ('title_menu', models.CharField(help_text=b"The 'menu title' of this section.", max_length=80)),
                ('slug', models.SlugField(max_length=80, verbose_name='Section Slug')),
                ('order', models.PositiveIntegerField(help_text=b'The order this page appears on the parent page.', verbose_name='Order')),
                ('content', textplusstuff.fields.TextPlusStuffField(help_text=b'The content of this page section.', null=True, verbose_name='Content', blank=True)),
                ('twitter_share_text', models.CharField(help_text=b"The text to use when sharing this page to Twitter. Limited to 110 characters. If this field is blank the text entered in the the parent page's Twitter Share Text will be used.", max_length=110, verbose_name='Twitter Share Text', blank=True)),
                ('page', models.ForeignKey(related_name='sections', verbose_name='Page', to='stacks_page.StacksPage')),
            ],
            options={
                'ordering': ('page', 'order'),
                'verbose_name': 'Page Section',
                'verbose_name_plural': 'Page Sections',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stackspagesection',
            unique_together=set([('page', 'slug')]),
        ),
    ]
