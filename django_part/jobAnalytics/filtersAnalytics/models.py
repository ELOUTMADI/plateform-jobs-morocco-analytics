# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Companies(models.Model):
    companyid = models.AutoField(db_column='companyID', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(blank=True, null=True)
    company_size = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companies'


class Expertise(models.Model):
    expertiseid = models.AutoField(db_column='expertiseID', primary_key=True)  # Field name made lowercase.
    expertise = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expertise'


class Hirers(models.Model):
    hirerid = models.AutoField(db_column='hirerID', primary_key=True)  # Field name made lowercase.
    hiring_team_name = models.CharField(blank=True, null=True)
    hirer_job_title = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hirers'


class JobConditions(models.Model):
    conditionid = models.AutoField(db_column='conditionID', primary_key=True)  # Field name made lowercase.
    promoted_status = models.CharField(blank=True, null=True)
    easy_apply_status = models.CharField(blank=True, null=True)
    is_reposted = models.BooleanField(blank=True, null=True)
    time_posted = models.CharField(blank=True, null=True)
    scrapping_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_conditions'


class JobDescriptions(models.Model):
    descriptionid = models.AutoField(db_column='descriptionID', primary_key=True)  # Field name made lowercase.
    job_description = models.TextField(blank=True, null=True)
    list_of_skills = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'job_descriptions'


class JobListings(models.Model):
    jobid = models.BigAutoField(db_column='JobID', primary_key=True)  # Field name made lowercase.
    companyid = models.ForeignKey(Companies, models.DO_NOTHING, db_column='companyID', blank=True, null=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Locations', models.DO_NOTHING, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    hirerid = models.ForeignKey(Hirers, models.DO_NOTHING, db_column='hirerID', blank=True, null=True)  # Field name made lowercase.
    jobtypeid = models.ForeignKey('JobTypes', models.DO_NOTHING, db_column='jobTypeID', blank=True, null=True)  # Field name made lowercase.
    sectorid = models.ForeignKey('Sectors', models.DO_NOTHING, db_column='sectorID', blank=True, null=True)  # Field name made lowercase.
    expertiseid = models.ForeignKey(Expertise, models.DO_NOTHING, db_column='expertiseID', blank=True, null=True)  # Field name made lowercase.
    descriptionid = models.ForeignKey(JobDescriptions, models.DO_NOTHING, db_column='descriptionID', blank=True, null=True)  # Field name made lowercase.
    conditionid = models.ForeignKey(JobConditions, models.DO_NOTHING, db_column='conditionID', blank=True, null=True)  # Field name made lowercase.
    jobidlinkedin = models.BigIntegerField(db_column='jobIDLinkedin', blank=True, null=True)  # Field name made lowercase.
    applicants = models.IntegerField(blank=True, null=True)
    years_experience = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_listings'


class JobTypes(models.Model):
    jobtypeid = models.AutoField(db_column='jobTypeID', primary_key=True)  # Field name made lowercase.
    job_type = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job_types'


class Locations(models.Model):
    locationid = models.AutoField(db_column='locationID', primary_key=True)  # Field name made lowercase.
    city = models.CharField(blank=True, null=True)
    remote_status = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Sectors(models.Model):
    sectorid = models.AutoField(db_column='sectorID', primary_key=True)  # Field name made lowercase.
    sector = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sectors'
