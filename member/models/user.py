from django.db import models


class Users(models.Model):
    pk = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(max_length=255)
    admin = models.IntegerField()
    id = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    password_key = models.CharField(db_column='passwordKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sign_key = models.CharField(db_column='signKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tp = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updated_at = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'