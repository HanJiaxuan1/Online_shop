# Generated by Django 3.1.7 on 2021-03-21 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_desc', models.TextField()),
                ('category', models.CharField(max_length=255)),
                ('sub_category', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('publish_date', models.DateField()),
                ('product_image', models.ImageField(upload_to='shop/images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('user_status', models.CharField(choices=[('normal', 'NORMAL'), ('vip', 'VIP')], default='active', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.CharField(default='', max_length=255)),
                ('date', models.CharField(default='', max_length=255)),
                ('status', models.CharField(choices=[('active', 'ACTIVE'), ('shipped', 'SHIPPED'), ('deliver', 'DELIVER')], default='active', max_length=255)),
                ('ordered_item', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.user')),
            ],
        ),
    ]
