# Generated by Django 4.0.6 on 2022-07-23 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_post_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, default='images/img-1.jpg', null=True, upload_to=''),
        ),
    ]