# Generated by Django 3.1.7 on 2021-04-10 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20210408_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='show_table_of_contents',
        ),
    ]
