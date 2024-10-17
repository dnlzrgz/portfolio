from django.db import models
from wagtail import blocks
from wagtail.models import Page, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


@register_setting
class ContactEmailSettings(BaseGenericSetting):
    email = models.EmailField(blank=True)

    panels = [FieldPanel("email")]


@register_setting
class FooterSettings(BaseGenericSetting):
    content = models.CharField(blank=True, max_length=255)
    location = models.CharField(blank=True, max_length=255)
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
        FieldPanel("content"),
        FieldPanel("location"),
        FieldPanel("copy"),
        FieldPanel("links"),
    ]
