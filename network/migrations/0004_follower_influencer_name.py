# Generated by Django 4.0.5 on 2022-08-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_like_twit_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='influencer_name',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
    ]
