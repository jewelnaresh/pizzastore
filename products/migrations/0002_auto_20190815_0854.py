# Generated by Django 2.2.3 on 2019-08-15 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('c', 'Cold Drinks'), ('p', 'Pizza'), ('d', 'Deserts')], default='p', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('d', 'danger'), ('p', 'primary'), ('s', 'secondary')], default='p', max_length=1),
            preserve_default=False,
        ),
    ]
