# Generated by Django 3.0.6 on 2020-07-17 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200715_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credits',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
