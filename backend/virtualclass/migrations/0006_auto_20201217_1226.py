# Generated by Django 3.1.3 on 2020-12-17 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualclass', '0005_auto_20201214_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='balance',
            field=models.DecimalField(decimal_places=4, default=1000, editable=False, max_digits=19),
        ),
    ]