# Generated by Django 5.0.6 on 2024-06-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_alter_service_image_alter_service_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.CharField(max_length=100),
        ),
    ]
