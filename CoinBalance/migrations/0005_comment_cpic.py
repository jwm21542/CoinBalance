# Generated by Django 4.2.4 on 2023-09-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoinBalance', '0004_comment_cdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='cpic',
            field=models.FileField(default=None, upload_to=''),
            preserve_default=False,
        ),
    ]
