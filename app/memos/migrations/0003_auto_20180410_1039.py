# Generated by Django 2.0.4 on 2018-04-10 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0002_auto_20180410_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memos',
            name='name_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
