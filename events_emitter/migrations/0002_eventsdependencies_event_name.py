# Generated by Django 2.0.1 on 2020-02-09 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_emitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventsdependencies',
            name='event_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
