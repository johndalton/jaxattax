# Generated by Django 3.2.3 on 2021-05-20 23:27

from django.db import migrations
import jaxattax.common.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_wagtailmetadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=jaxattax.common.models.StreamField([]),
        ),
        migrations.AlterField(
            model_name='page',
            name='body',
            field=jaxattax.common.models.StreamField([]),
        ),
    ]