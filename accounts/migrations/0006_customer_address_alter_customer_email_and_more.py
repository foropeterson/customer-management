# Generated by Django 4.1.5 on 2023-07-10 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor')], max_length=200, null=True),
        ),
    ]