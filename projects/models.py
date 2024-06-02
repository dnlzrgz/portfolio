from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db import models
from django.core.paginator import Paginator
from django.utils import timezone
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail.signals import page_published
from wagtail.contrib.frontend_cache.utils import PurgeBatch


class ProjectsIndexPage(Page):
    subpage_types = ["projects.ProjectPage"]

    def get_projets_items(self):
        return Paginator(self.get_children().live(), 10)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        projects = self.get_children().live().order_by("-first_published_at")
        context["projects"] = projects
        return context

    def get_cached_paths(self):
        yield "/"

        for page_number in range(1, self.get_projets_items().num_pages + 1):
            yield "/?page=" + str(page_number)


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


def project_page_changed(project_page):
    batch = PurgeBatch()
    for projects_index in ProjectsIndexPage.objects.live():
        if project_page in projects_index.get_projets_items().object_list:
            batch.add_page(ProjectsIndexPage)

    batch.purge()


@receiver(page_published, sender=ProjectPage)
def project_published_handler(instance, **kwargs):
    project_page_changed(instance)


@receiver(pre_delete, sender=ProjectPage)
def project_deleted_handler(instance, **kwargs):
    project_page_changed(instance)
