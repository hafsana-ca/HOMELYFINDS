# Generated by Django 5.1 on 2024-09-10 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Adminapp', '0007_productdb_is_deal_of_the_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotDealDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('products', models.ManyToManyField(to='Adminapp.productdb')),
            ],
        ),
    ]
