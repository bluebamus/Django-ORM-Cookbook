# Generated by Django 4.1.3 on 2022-12-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='benevolence_factor',
            field=models.PositiveSmallIntegerField(default=50, help_text='How benevolent this hero is?'),
        ),
    ]