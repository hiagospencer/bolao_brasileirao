# Generated by Django 5.1.2 on 2024-10-28 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0022_palpite_tipo_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palpite',
            name='tipo_class',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
