# Generated by Django 3.0.6 on 2020-07-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hacks', '0002_auto_20200714_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacks',
            name='fee',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='hacks',
            name='team_personnel',
            field=models.PositiveIntegerField(blank=True, default=5, null=True),
        ),
    ]