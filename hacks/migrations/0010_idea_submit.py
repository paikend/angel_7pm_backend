# Generated by Django 3.0.6 on 2020-07-17 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hacks', '0009_auto_20200717_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_url', models.TextField(blank=True, null=True)),
                ('demo_url', models.TextField(blank=True, null=True)),
                ('pitching_url', models.TextField(blank=True, null=True)),
                ('present_url', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='지원일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일')),
                ('hacks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hacks.Hacks')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hacks.Team')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='지원일')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정일')),
                ('hacks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hacks.Hacks')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hacks.Team')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
