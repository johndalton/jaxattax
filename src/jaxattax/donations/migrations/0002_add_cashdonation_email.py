# Generated by Django 3.1.7 on 2021-04-11 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashdonation',
            name='email',
            field=models.EmailField(blank=True, help_text='The email address entered in the Stripe payment. Not required for manually entered donations.', max_length=254),
        ),
        migrations.AddField(
            model_name='cashdonation',
            name='receipt_sent',
            field=models.BooleanField(default=False, help_text='Has an automatic receipt been emailed?'),
        ),
        migrations.AlterField(
            model_name='cashdonation',
            name='stripe_id',
            field=models.CharField(blank=True, help_text='The ID of the payment in Stripe, if it was done online.', max_length=100),
        ),
    ]
