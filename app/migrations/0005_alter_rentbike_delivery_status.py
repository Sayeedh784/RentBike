# Generated by Django 4.0.2 on 2022-03-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rentbike_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentbike',
            name='delivery_status',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]