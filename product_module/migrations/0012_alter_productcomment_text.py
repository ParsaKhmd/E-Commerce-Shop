# Generated by Django 4.1.6 on 2024-04-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0011_productcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='text',
            field=models.TextField(null=True, verbose_name='متن نظر'),
        ),
    ]
