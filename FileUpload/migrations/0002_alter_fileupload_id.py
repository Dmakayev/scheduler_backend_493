# Generated by Django 4.0.2 on 2022-04-14 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileUpload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
