# Generated by Django 4.0.6 on 2023-10-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_alter_account_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, default='img-3.jpg', null=True, upload_to='post/'),
        ),
    ]