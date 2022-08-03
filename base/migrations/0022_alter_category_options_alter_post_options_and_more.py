# Generated by Django 4.0.6 on 2022-07-24 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_category_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]