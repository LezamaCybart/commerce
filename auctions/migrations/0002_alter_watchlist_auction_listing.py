# Generated by Django 3.2.4 on 2021-06-25 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auction_listing',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='auctions.Auction_listing'),
        ),
    ]
