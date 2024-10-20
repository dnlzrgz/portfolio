# Generated by Django 5.1 on 2024-08-13 14:27

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', 0), ('subheading', 0), ('quote', 1), ('paragraph', 2), ('code', 5), ('image', 6), ('embed', 7)], block_lookup={0: ('wagtail.blocks.TextBlock', (), {}), 1: ('wagtail.blocks.BlockQuoteBlock', (), {}), 2: ('wagtail.blocks.RichTextBlock', (), {'editor': 'full'}), 3: ('wagtail.blocks.CharBlock', (), {}), 4: ('wagtail.blocks.RichTextBlock', (), {'features': []}), 5: ('wagtail.blocks.StructBlock', [[('language', 3), ('code', 4)]], {'label': 'Code'}), 6: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 7: ('wagtail.embeds.blocks.EmbedBlock', (), {})}),
        ),
    ]
