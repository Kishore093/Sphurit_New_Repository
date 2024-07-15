# Generated by Django 4.2 on 2023-11-02 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_wallettransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransaction',
            name='bank',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bank_transactions', to='core.banks'),
        ),
        migrations.AlterField(
            model_name='wallettransaction',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallet_transactions', to='core.wallet'),
        ),
    ]
