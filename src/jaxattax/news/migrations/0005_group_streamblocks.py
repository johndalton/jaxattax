# Generated by Django 3.1.7 on 2021-04-12 12:38
from django.db import migrations

from jaxattax.utils.migrations import StreamFieldDataMigration


def rename_block(from_name, to_name, blocks):
    for block in blocks:
        if block['type'] == from_name:
            block = block.copy()
            block['type'] = to_name
        yield block


def forwards(instance, data):
    return list(rename_block('large_image', 'captioned_image', data))


def backwards(instance, data):
    return list(rename_block('captioned_image', 'large_image', data))


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_newsitem_blocks'),
    ]

    operations = [
        StreamFieldDataMigration(
            model_name='newsitem',
            name='body',
            forwards_code=forwards,
            backwards_code=backwards,
        ),
    ]
