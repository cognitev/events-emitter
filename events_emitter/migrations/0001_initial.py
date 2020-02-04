# Generated by Django 3.0.3 on 2020-02-06 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=80)),
                ('state', models.CharField(choices=[('PRESENT', 'PRESENT'), ('ABSENT', 'ABSENT')], max_length=10)),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='EventsDependencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependency_experssion', models.CharField(max_length=250)),
            ],
        ),
    ]
