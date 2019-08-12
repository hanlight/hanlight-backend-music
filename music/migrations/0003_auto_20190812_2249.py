# Generated by Django 2.1.11 on 2019-08-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20190812_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='album_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
