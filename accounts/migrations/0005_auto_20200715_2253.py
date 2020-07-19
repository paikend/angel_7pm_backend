# Generated by Django 3.0.6 on 2020-07-15 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='belong_role',
            new_name='belong',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
