# Generated by Django 3.1 on 2020-08-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200806_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='note',
            field=models.CharField(default='Hello World', max_length=100, null=True),
        ),
    ]