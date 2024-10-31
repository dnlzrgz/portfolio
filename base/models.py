from django.db import models
from wagtail.models import Page, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from base.blocks import (
    AbstractBlock,
    CalendarBlock,
    ContactEmailBlock,
    FeaturedBlogPostBlock,
    FeaturedProjectBlock,
    ImageBlock,
    NoteBlock,
    SocialMediaLinksBlock,
    StackListBlock,
    TodoListBlock,
)


class HomePage(Page):
    widgets = StreamField(
        [
            ("abstract", AbstractBlock()),
            ("calendar", CalendarBlock()),
            ("contact_email", ContactEmailBlock()),
            ("featured_blog_post", FeaturedBlogPostBlock()),
            ("featured_project", FeaturedProjectBlock()),
            ("image", ImageBlock()),
            ("note", NoteBlock()),
            ("social_media_links", SocialMediaLinksBlock()),
            ("stack_list", StackListBlock()),
            ("todo_list", TodoListBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("widgets"),
    ]

    subpage_types = [
        "base.StaticPage",
        "blog.BlogIndexPage",
        "projects.ProjectsIndexPage",
    ]


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    parent_page_types = ["base.HomePage"]
    subpage_types = []


@register_setting(icon="mail")
class ContactEmailSettings(BaseGenericSetting):
    email = models.EmailField(blank=True)

    panels = [FieldPanel("email")]


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
