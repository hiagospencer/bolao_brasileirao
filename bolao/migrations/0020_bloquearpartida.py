# Generated by Django 5.1.2 on 2024-10-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bolao', '0019_alter_verificacao_verificado'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloquearPartida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rodada_bloqueada', models.BooleanField(default=False)),
            ],
        ),
    ]
