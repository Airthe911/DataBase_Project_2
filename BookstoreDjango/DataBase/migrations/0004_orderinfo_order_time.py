# Generated by Django 4.1.7 on 2023-12-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0003_remove_book_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='order_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
