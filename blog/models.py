from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index


class BlogIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        posts = self.get_children().live().order_by("-first_published_at")
        context["posts"] = posts
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPostPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogPostPage(Page):
    tldr = RichTextField(features=[], blank=True)
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
    )

    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("tldr"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("tldr"),
                FieldPanel("tags"),
            ],
            heading="Post information",
        ),
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        posts = BlogPostPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context["posts"] = posts
        return context
