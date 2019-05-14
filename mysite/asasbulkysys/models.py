from __future__ import unicode_literals

from django.db import models


class AddressBook(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=6, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    ward = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = 'address_book'


class CampaignEndDay(models.Model):
    campaign = models.ForeignKey('Campaigns', primary_key=True)
    campaign_end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'campaign_end_day'


class CampaignStartDay(models.Model):
    campaign = models.ForeignKey('Campaigns', primary_key=True)
    campaign_start_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'campaign_start_day'


class Campaigns(models.Model):
    campaign_id = models.IntegerField(primary_key=True)
    campaign_name = models.CharField(max_length=200, blank=True)
    campaign_descr = models.CharField(max_length=500, blank=True)
    date_created = models.DateField()
    delivery_mechanism = models.CharField(max_length=8)
    campaign_category = models.CharField(max_length=2, blank=True)
    target_level = models.CharField(max_length=15, blank=True)
    is_campaign_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaigns'


class CampaignsDefinedMessages(models.Model):
    campaign_message_id = models.IntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaigns, blank=True, null=True)
    message_txt = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'campaigns_defined_messages'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class EmailDetails(models.Model):
    email_id = models.IntegerField(primary_key=True)
    email_address = models.CharField(max_length=50, blank=True)
    is_it_primary_email = models.IntegerField()
    contact = models.ForeignKey(AddressBook, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email_details'


class Feedback(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    recipient_mobile = models.CharField(max_length=20, blank=True)
    message = models.CharField(max_length=1000, blank=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


class GroupMembers(models.Model):
    group = models.ForeignKey('Groups')
    contact = models.ForeignKey(AddressBook)

    class Meta:
        managed = False
        db_table = 'group_members'


class Groups(models.Model):
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=50, blank=True)
    group_description = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'groups'


class IndividualizedReminders(models.Model):
    individualized_reminders_id = models.IntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaigns, blank=True, null=True)
    contact = models.ForeignKey(AddressBook, blank=True, null=True)
    reminder_end_date = models.DateField(blank=True, null=True)
    event_deadline_date = models.DateField(blank=True, null=True)
    no_running_days = models.IntegerField(blank=True, null=True)
    reason_for_reminder = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'individualized_reminders'


class MobileDetails(models.Model):
    mobile_id = models.IntegerField(primary_key=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    is_it_primary_number = models.IntegerField()
    contact = models.ForeignKey(AddressBook, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mobile_details'


class SelectedDaysOfDelivery(models.Model):
    selected_day_id = models.IntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaigns, blank=True, null=True)
    selected_day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'selected_days_of_delivery'


class SelectedTimeOfDelivery(models.Model):
    campaign = models.ForeignKey(Campaigns)
    selected_time = models.TimeField()

    class Meta:
        managed = False
        db_table = 'selected_time_of_delivery'


class SmsCampaignTargetedGroups(models.Model):
    group = models.ForeignKey(Groups)
    campaign = models.ForeignKey(Campaigns)

    class Meta:
        managed = False
        db_table = 'sms_campaign_targeted_groups'


class SmsSignatures(models.Model):
    sms_signature_id = models.IntegerField(primary_key=True)
    signature_content = models.CharField(max_length=50, blank=True)
    signature_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_signatures'


class SmsTemplateCategories(models.Model):
    template_category_id = models.IntegerField(primary_key=True)
    template_category_name = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'sms_template_categories'


class SmsTemplates(models.Model):
    sms_template_id = models.IntegerField(primary_key=True)
    template_class = models.ForeignKey(SmsTemplateCategories, blank=True, null=True)
    template_content = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'sms_templates'
