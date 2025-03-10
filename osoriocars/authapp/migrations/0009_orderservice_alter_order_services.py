# Generated by Django 5.0.6 on 2024-06-25 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_rename_name_service_title_alter_service_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.service')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(related_name='orders', through='authapp.OrderService', to='authapp.service'),
        ),
    ]
