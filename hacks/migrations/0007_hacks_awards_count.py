# Generated by Django 3.0.6 on 2020-07-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hacks', '0006_auto_20200715_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacks',
            name='awards_count',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
