# Generated by Django 4.0.1 on 2024-09-13 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KwentasApp', '0005_customuser_totp_secret_alter_customuser_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirebaseEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('ppa', models.CharField(max_length=255)),
            ],
        ),
    ]