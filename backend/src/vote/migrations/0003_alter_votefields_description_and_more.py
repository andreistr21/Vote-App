# Generated by Django 4.2.6 on 2023-11-06 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_alter_voteform_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votefields',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='voteform',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]