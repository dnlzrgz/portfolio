# Generated by Django 5.1.3 on 2024-11-19 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_contactemailsettings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='author_name',
            field=models.CharField(blank=True, help_text='Author name of the site.', max_length=255, verbose_name='Author name'),
        ),
    ]
