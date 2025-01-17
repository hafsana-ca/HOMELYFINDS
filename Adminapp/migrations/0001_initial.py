# Generated by Django 5.1 on 2024-09-01 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=50, null=True)),
                ('Description', models.CharField(blank=True, max_length=50, null=True)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='Category Images')),
            ],
        ),
    ]
