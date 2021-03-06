# Generated by Django 3.0.6 on 2020-07-17 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hacks', '0012_auto_20200718_0524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submit',
            name='hacks',
        ),
        migrations.RemoveField(
            model_name='submit',
            name='team',
        ),
        migrations.AddField(
            model_name='team',
            name='demo_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='github_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='pitching_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='present_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='service_detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='service_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='수정일'),
        ),
        migrations.DeleteModel(
            name='Idea',
        ),
        migrations.DeleteModel(
            name='Submit',
        ),
    ]
