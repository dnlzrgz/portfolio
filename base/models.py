from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.models import StreamField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)


@register_setting
class FooterSettings(BaseGenericSetting):
    copy = models.CharField(blank=True, max_length=255)
    links = StreamField(
        [
            (
                "url",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock()),
                        ("url", blocks.URLBlock()),
                    ]
                ),
            )
        ],
        blank=True,
    )

    panels = [
        FieldPanel("copy"),
        FieldPanel("links"),
    ]
