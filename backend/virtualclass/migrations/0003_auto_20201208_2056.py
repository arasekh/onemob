# Generated by Django 3.1.3 on 2020-12-08 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualclass', '0002_video_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=19),
        ),
    ]