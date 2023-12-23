# Generated by Django 4.1.7 on 2023-12-12 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('author', models.CharField(max_length=100, null=True)),
                ('publisher', models.CharField(blank=True, max_length=100, null=True)),
                ('original_title', models.CharField(max_length=100, null=True)),
                ('translator', models.CharField(max_length=100, null=True)),
                ('pub_year', models.CharField(max_length=100, null=True)),
                ('pages', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('currency_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('binding', models.CharField(blank=True, max_length=100, null=True)),
                ('isbn', models.CharField(blank=True, max_length=100, null=True)),
                ('author_intro', models.TextField()),
                ('book_intro', models.TextField()),
                ('content', models.TextField()),
                ('tags', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('store_id', models.CharField(blank=True, max_length=100, null=True)),
                ('book_id', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('number', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('state', models.DecimalField(decimal_places=0, max_digits=1, null=True)),
                ('payment_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('receipt_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(blank=True, max_length=100, null=True)),
                ('book_id', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('stock_level', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('terminal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User2Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('store_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]