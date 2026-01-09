

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('subcategory', models.CharField(blank=True, max_length=255, null=True)),
                ('edition', models.CharField(blank=True, max_length=255, null=True)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
                ('condition', models.CharField(blank=True, max_length=255, null=True)),
                ('market_value', models.FloatField(blank=True, null=True)),
                ('last_checked', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('subcategory', models.CharField(blank=True, max_length=255, null=True)),
                ('edition', models.CharField(blank=True, max_length=255, null=True)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
                ('condition', models.CharField(blank=True, max_length=255, null=True)),
                ('desired_price', models.FloatField(blank=True, null=True)),
                ('last_checked', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
