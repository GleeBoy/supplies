# Generated by Django 3.0 on 2021-01-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superclass',
            name='description',
            field=models.CharField(max_length=72, null=True, verbose_name='描述'),
        ),
    ]
