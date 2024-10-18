from django.db import models
from wagtail import blocks
from wagtail.models import ClusterableModel, Page, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


@register_setting(icon="mail")
class ContactEmailSettings(BaseGenericSetting):
    email = models.EmailField(blank=True)

    panels = [FieldPanel("email")]


@register_setting(icon="cog")
class FooterTextSettings(ClusterableModel, BaseGenericSetting):
    body = RichTextField(blank=True)

    panels = [
        FieldPanel("body"),
    ]


@register_setting(icon="cog")
class SocialMediaSettings(ClusterableModel, BaseGenericSetting):
    links = StreamField(
        [
            (
                "link",
                blocks.StructBlock(
                    [
                        ("name", blocks.CharBlock()),
                        ("url", blocks.URLBlock()),
                    ],
                ),
            )
        ],
        blank=True,
    )

    panels = [FieldPanel("links")]


@register_setting(icon="site")
class SiteSettings(BaseSiteSetting):
    title_suffix = models.CharField(
        verbose_name="Title suffix",
        max_length=255,
        help_text="The suffix for the title meta tag e.g. ' | dnlzrgz'",
        default="dnlzrgz",
    )

    panels = [
        FieldPanel("title_suffix"),
    ]
