# Generated by Django 4.1.7 on 2023-12-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0005_alter_orderinfo_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]