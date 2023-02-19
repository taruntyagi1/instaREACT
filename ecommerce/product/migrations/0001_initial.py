# Generated by Django 4.1.6 on 2023-02-05 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=1000, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=1000, unique=True)),
                ('image', models.FileField(blank=True, upload_to='photo/category')),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=1000, unique=True)),
                ('stock_record', models.IntegerField(blank=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('image', models.FileField(blank=True, upload_to='photo/products')),
                ('price', models.IntegerField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=1000, unique=True)),
                ('stock_record', models.IntegerField(blank=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('image', models.FileField(blank=True, upload_to='photo/variants')),
                ('price', models.IntegerField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variant', to='product.product')),
            ],
        ),
    ]