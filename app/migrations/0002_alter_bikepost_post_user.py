# Generated by Django 4.0.2 on 2022-02-24 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikepost',
            name='post_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer'),
        ),
    ]
