from django.db import models


class Graduates(models.Model):
    pk = models.AutoField(primary_key=True)
    user_pk = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_pk')
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'Graduates'