# Generated by Django 2.1 on 2018-08-18 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookracks', '0006_auto_20180816_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]