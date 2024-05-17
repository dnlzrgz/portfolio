from django.db import models
from wagtail import blocks
from wagtail.models import Page, StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    # Hero section
    hero_overtitle = models.CharField(max_length=255, blank=True)
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)

    # Project showcase section
    projects_overtitle = models.CharField(max_length=255, blank=True)
    projects_title = models.CharField(max_length=255, blank=True)
    projects_content = RichTextField(features=[], blank=True)
    featured_projects = StreamField(
        [
            (
                "project",
                blocks.PageChooserBlock(target_model="projects.ProjectPage"),
            ),
        ],
        blank=True,
    )

    # Blog posts
    blog_overtitle = models.CharField(max_length=255, blank=True)
    blog_title = models.CharField(max_length=255, blank=True)
    blog_content = RichTextField(features=[], blank=True)
    featured_posts = StreamField(
        [
            (
                "post",
                blocks.PageChooserBlock(target_model="blog.BlogPostPage"),
            ),
        ],
        blank=True,
    )

    # Biography
    bio_overtitle = models.CharField(max_length=255, blank=True)
    bio_title = models.CharField(max_length=255, blank=True)
    bio_content = RichTextField(features=[], blank=True)

    # Contact
    contact_overtitle = models.CharField(max_length=255, blank=True)
    contact_title = models.CharField(max_length=255, blank=True)
    contact_content = RichTextField(features=[], blank=True)
    contact_email = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_overtitle"),
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("projects_overtitle"),
                FieldPanel("projects_title"),
                FieldPanel("projects_content"),
                FieldPanel("featured_projects"),
            ],
            heading="Projects",
        ),
        MultiFieldPanel(
            [
                FieldPanel("blog_overtitle"),
                FieldPanel("blog_title"),
                FieldPanel("blog_content"),
                FieldPanel("featured_posts"),
            ],
            heading="Blog",
        ),
        MultiFieldPanel(
            [
                FieldPanel("bio_overtitle"),
                FieldPanel("bio_title"),
                FieldPanel("bio_content"),
            ],
            heading="Biography",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_overtitle"),
                FieldPanel("contact_title"),
                FieldPanel("contact_content"),
                FieldPanel("contact_email"),
            ],
            heading="Contact",
        ),
    ]
