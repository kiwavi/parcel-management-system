# Generated by Django 3.2.9 on 2022-08-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcelapp', '0009_auto_20220405_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='parcel_number',
            field=models.CharField(max_length=64),
        ),
    ]
