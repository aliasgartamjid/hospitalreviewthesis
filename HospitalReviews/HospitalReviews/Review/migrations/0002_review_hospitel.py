# Generated by Django 4.1.3 on 2023-05-20 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='hospitel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Review.hospital'),
            preserve_default=False,
        ),
    ]
