# Generated by Django 5.1 on 2024-09-04 04:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0003_role_can_view_streams_role_can_view_users_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='custom_can_view_streams',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='custom_can_view_users',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userrole',
            name='custom_has_full_access',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='newapp.role'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to=settings.AUTH_USER_MODEL),
        ),
    ]
