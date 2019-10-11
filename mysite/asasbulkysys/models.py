# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
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
    company = models.ForeignKey('Companies')

    class Meta:
        managed = False
        db_table = 'address_book'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


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
    company = models.ForeignKey('Companies')

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


class Companies(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100, blank=True)
    business_descr = models.CharField(max_length=500, blank=True)
    postal_address = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=50, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=50, blank=True)
    mobile_verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'companies'


class CompanyUsers(models.Model):
    company = models.ForeignKey(Companies, blank=True, null=True)
    user = models.ForeignKey(AuthUser, primary_key=True)

    class Meta:
        managed = False
        db_table = 'company_users'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    recipient_contact_id = models.CharField(max_length=20, blank=True)
    recipient_name = models.CharField(max_length=200, blank=True)
    recipient_group_id = models.IntegerField(blank=True, null=True)
    recipient_campaign_id = models.IntegerField(blank=True, null=True)
    scheduled_time = models.TimeField(blank=True, null=True)
    scheduled_date = models.DateField(blank=True, null=True)
    delivery_note = models.CharField(max_length=100, blank=True)
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
    company = models.ForeignKey(Companies)

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
