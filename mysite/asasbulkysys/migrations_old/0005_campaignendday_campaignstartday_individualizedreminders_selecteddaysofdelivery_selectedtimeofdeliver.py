# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asasbulkysys', '0004_auto_20190511_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignEndDay',
            fields=[
            ],
            options={
                'db_table': 'campaign_end_day',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampaignStartDay',
            fields=[
            ],
            options={
                'db_table': 'campaign_start_day',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualizedReminders',
            fields=[
            ],
            options={
                'db_table': 'individualized_reminders',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SelectedDaysOfDelivery',
            fields=[
            ],
            options={
                'db_table': 'selected_days_of_delivery',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SelectedTimeOfDelivery',
            fields=[
            ],
            options={
                'db_table': 'selected_time_of_delivery',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmsCampaignTargetedGroups',
            fields=[
            ],
            options={
                'db_table': 'sms_campaign_targeted_groups',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
