# Generated by Django 3.1.7 on 2021-04-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210411_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/%Y%m%d'),
        ),
    ]
