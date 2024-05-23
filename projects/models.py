from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


class ProjectsIndexPage(Page):
    subpage_types = ["projects.ProjectPage"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        projects = self.get_children().live().order_by("-first_published_at")
        context["projects"] = projects
        return context


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "ProjectPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class ProjectPage(Page):
    description = RichTextField(editor="minimal", blank=True)
    date = models.DateField(default=timezone.now)
    repository_url = models.URLField(blank=True)
    page_url = models.URLField(blank=True)
    tags = ClusterTaggableManager(
        through=ProjectPageTag,
        blank=True,
    )

    body = RichTextField(editor="full", blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("description"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("description"),
                FieldPanel("date"),
                FieldPanel("repository_url"),
                FieldPanel("page_url"),
                FieldPanel("tags"),
            ],
            heading="Project information",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["projects.ProjectsIndexPage"]
    subpage_types = []
