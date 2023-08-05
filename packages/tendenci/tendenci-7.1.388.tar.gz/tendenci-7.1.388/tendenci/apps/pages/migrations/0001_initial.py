# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tagging.fields
import tendenci.apps.user_groups.utils
import tendenci.apps.base.fields
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meta', '0001_initial'),
        ('entities', '0001_initial'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderImage',
            fields=[
                ('file_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='files.File')),
            ],
            bases=('files.file',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allow_anonymous_view', models.BooleanField(default=True, verbose_name='Public can view')),
                ('allow_user_view', models.BooleanField(default=True, verbose_name='Signed in user can view')),
                ('allow_member_view', models.BooleanField(default=True)),
                ('allow_user_edit', models.BooleanField(default=False, verbose_name='Signed in user can change')),
                ('allow_member_edit', models.BooleanField(default=False)),
                ('create_dt', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('update_dt', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
                ('creator_username', models.CharField(max_length=50)),
                ('owner_username', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True, verbose_name=b'Active')),
                ('status_detail', models.CharField(default=b'active', max_length=50)),
                ('guid', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=500, blank=True)),
                ('slug', tendenci.apps.base.fields.SlugField(max_length=100, verbose_name='URL Path', db_index=True)),
                ('content', tinymce.models.HTMLField()),
                ('view_contact_form', models.BooleanField(default=False)),
                ('design_notes', models.TextField(verbose_name='Design Notes', blank=True)),
                ('syndicate', models.BooleanField(default=False, verbose_name='Include in RSS feed')),
                ('template', models.CharField(max_length=50, verbose_name='Template', blank=True)),
                ('tags', tagging.fields.TagField(max_length=255, blank=True)),
                ('contributor_type', models.IntegerField(default=1, choices=[(1, 'Author'), (2, 'Publisher')])),
                ('google_profile', models.URLField(verbose_name='Google+ URL', blank=True)),
                ('creator', models.ForeignKey(related_name='pages_page_creator', on_delete=django.db.models.deletion.SET_NULL, default=None, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('entity', models.ForeignKey(related_name='pages_page_entity', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='entities.Entity', null=True)),
                ('group', models.ForeignKey(default=tendenci.apps.user_groups.utils.get_default_group, to='user_groups.Group', null=True)),
                ('header_image', models.ForeignKey(to='pages.HeaderImage', null=True)),
                ('meta', models.OneToOneField(null=True, to='meta.Meta')),
                ('owner', models.ForeignKey(related_name='pages_page_owner', on_delete=django.db.models.deletion.SET_NULL, default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'permissions': (('view_page', 'Can view page'),),
            },
        ),
    ]
