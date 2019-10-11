# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asasbulkysys', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressBook',
            fields=[
            ],
            options={
                'db_table': 'address_book',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaigns',
            fields=[
            ],
            options={
                'db_table': 'campaigns',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampaignsDefinedMessages',
            fields=[
            ],
            options={
                'db_table': 'campaigns_defined_messages',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailDetails',
            fields=[
            ],
            options={
                'db_table': 'email_details',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
            ],
            options={
                'db_table': 'feedback',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
            ],
            options={
                'db_table': 'group_members',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
            ],
            options={
                'db_table': 'groups',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MobileDetails',
            fields=[
            ],
            options={
                'db_table': 'mobile_details',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmsSignatures',
            fields=[
            ],
            options={
                'db_table': 'sms_signatures',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmsTemplateCategories',
            fields=[
            ],
            options={
                'db_table': 'sms_template_categories',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmsTemplates',
            fields=[
            ],
            options={
                'db_table': 'sms_templates',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
