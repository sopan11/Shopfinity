# Generated by Django 5.1.7 on 2025-04-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='adminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=20, null=True)),
                ('last_name', models.TextField(max_length=20, null=True)),
                ('email', models.TextField(max_length=40)),
                ('password', models.TextField(max_length=20)),
            ],
        ),
    ]
