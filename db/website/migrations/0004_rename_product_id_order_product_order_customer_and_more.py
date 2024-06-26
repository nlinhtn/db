# Generated by Django 4.2.13 on 2024-06-04 06:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product_id',
            new_name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='done', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=25, max_digits=19),
            preserve_default=False,
        ),
    ]
