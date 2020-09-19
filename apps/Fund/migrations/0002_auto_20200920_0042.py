# Generated by Django 3.1.1 on 2020-09-20 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Fund', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fundhistoricalnetworthranking',
            old_name='update_date',
            new_name='current_date',
        ),
        migrations.AlterUniqueTogether(
            name='fundhistoricalnetworthranking',
            unique_together={('fund_code', 'current_date')},
        ),
    ]
