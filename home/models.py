from django.db import models
from wagtail import blocks
from wagtail.models import Page, StreamField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    # Hero section
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_cta_text = models.CharField(max_length=255, blank=True)
    hero_cta_url = models.URLField(blank=True)

    # Biography
    biography = RichTextField(editor="minimal", blank=True)

    # Project showcase section
    projects_title = models.CharField(max_length=255, blank=True)
    projects_subtitle = RichTextField(editor="minimal", blank=True)
    featured_projects = StreamField(
        [
            (
                "project",
                blocks.PageChooserBlock(
                    target_model="projects.ProjectPage",
                ),
            ),
        ],
        blank=True,
    )

    # Stack section
    stack_title = models.CharField(max_length=255, blank=True)
    stack_subtitle = RichTextField(editor="minimal", blank=True)
    stack_stack = StreamField(
        [
            ("item", blocks.CharBlock()),
        ],
        blank=True,
    )

    # Contact section
    contact_title = models.CharField(max_length=255, blank=True)
    contact_subtitle = RichTextField(editor="minimal", blank=True)
    contact_content = RichTextField(editor="minimal", blank=True)
    contact_cta = RichTextField(editor="minimal", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_cta_text"),
                FieldPanel("hero_cta_url"),
            ],
            heading="Hero",
        ),
        FieldPanel("biography"),
        MultiFieldPanel(
            [
                FieldPanel("projects_title"),
                FieldPanel("projects_subtitle"),
                FieldPanel("featured_projects"),
            ],
            heading="Projects",
        ),
        MultiFieldPanel(
            [
                FieldPanel("contact_title"),
                FieldPanel("contact_subtitle"),
                FieldPanel("contact_content"),
                FieldPanel("contact_cta"),
            ],
            heading="Contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("stack_title"),
                FieldPanel("stack_subtitle"),
                FieldPanel("stack_stack"),
            ],
            heading="Stack",
        ),
    ]
