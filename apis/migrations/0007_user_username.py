# Generated by Django 5.0.4 on 2024-04-17 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_rename_token_refreshtoken_refresh_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=False, max_length=255),
            preserve_default=False,
        ),
    ]
