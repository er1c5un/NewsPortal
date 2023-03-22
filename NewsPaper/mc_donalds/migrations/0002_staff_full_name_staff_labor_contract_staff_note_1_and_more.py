# Generated by Django 4.1.6 on 2023-02-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_donalds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='full_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='staff',
            name='labor_contract',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='staff',
            name='note_1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='position',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
