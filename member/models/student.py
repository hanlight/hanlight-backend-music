from django.db import models


class Students(models.Model):
    pk = models.AutoField(primary_key=True)
    user_pk = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_pk')
    name = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    grade = models.IntegerField()
    class_num = models.IntegerField(db_column='classNum')  # Field name made lowercase.
    student_num = models.IntegerField(db_column='studentNum')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Students'