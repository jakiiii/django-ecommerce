# Generated by Django 2.1.1 on 2018-09-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20180927_2102'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductManager',
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
