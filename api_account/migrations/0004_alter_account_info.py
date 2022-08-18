# Generated by Django 3.2.8 on 2022-06-16 07:50
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api_account', '0003_migrate_role_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='address',
        ),
        migrations.RemoveField(
            model_name='account',
            name='age',
        ),
        migrations.RemoveField(
            model_name='account',
            name='phone',
        ),
        migrations.AddField(
            model_name='role',
            name='is_activate',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True,
                                      help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                      verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_account.role'),
        ),
        migrations.AddField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='account',
            name='is_activate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
