# Generated by Django 4.0.5 on 2022-06-29 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='writer',
        ),
    ]
