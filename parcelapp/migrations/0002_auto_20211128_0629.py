# Generated by Django 3.1.4 on 2021-11-28 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcelapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
