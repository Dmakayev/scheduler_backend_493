# Generated by Django 4.0.2 on 2022-04-14 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CourseTables', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempCourse',
            fields=[
                ('classNumber', models.TextField()),
                ('className', models.TextField()),
                ('credits', models.TextField()),
                ('sectionNumber', models.TextField()),
                ('capacity', models.TextField()),
                ('room', models.TextField()),
                ('waitSize', models.TextField()),
                ('enrollment', models.TextField()),
                ('days', models.TextField()),
                ('uniqueCourseID', models.TextField(primary_key=True, serialize=False)),
                ('time', models.TextField()),
                ('instructor', models.TextField()),
            ],
        ),
    ]
