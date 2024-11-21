from django.core.paginator import Paginator
from django.db import models
from django.db.models.fields import datetime
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, StreamField
from wagtail.search import index
from wagtail.signals import page_published


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("bash", "bash"),
            ("c", "c"),
            ("css", "css"),
            ("django", "django"),
            ("go", "golang"),
            ("html", "html"),
            ("java", "java"),
            ("javascript", "javascript"),
            ("json", "json"),
            ("makefile", "makefile"),
            ("markdown", "markdown"),
            ("nginx", "nginx"),
            ("php", "php"),
            ("plaintext", "plaintext"),
            ("python", "python"),
            ("rust", "rust"),
            ("sql", "sql"),
            ("yaml", "yaml"),
            ("zsh", "zsh"),
        ]
    )
    code = blocks.TextBlock()

    class Meta:
        icon = "code"
        template = "blocks/code_block.html"


class BlogIndexPage(Page):
    parent_page_types = ["base.HomePage"]
    subpage_types = ["blog.BlogPostPage"]

    def get_blog_items(self):
        return Paginator(self.get_children().live(), 10)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        posts = self.get_children().live().order_by("-first_published_at")
        context["posts"] = posts
        return context

    def get_cached_paths(self):
        yield "/"

        for page_number in range(1, self.get_blog_items().num_pages + 1):
            yield "/?page=" + str(page_number)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPostPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogPostPage(Page):
    date = models.DateField(default=datetime.date.today)
    tldr = RichTextField(blank=True)
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
    )

    body = StreamField(
        [
            ("heading", blocks.TextBlock()),
            ("subheading", blocks.TextBlock()),
            ("quote", blocks.BlockQuoteBlock()),
            ("paragraph", blocks.RichTextBlock()),
            ("code", CodeBlock(label="Code")),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
        ],
    )

    search_fields = Page.search_fields + [
        index.SearchField("tldr"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
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


def blog_page_changed(blog_page):
    batch = PurgeBatch()
    for blog_index in BlogIndexPage.objects.live():
        if blog_page in blog_index.get_blog_items().object_list:
            batch.add_page(blog_index)

    batch.purge()


@receiver(page_published, sender=BlogPostPage)
def blog_published_handler(instance, **kwargs):
    blog_page_changed(instance)


@receiver(pre_delete, sender=BlogPostPage)
def blog_deleted_handler(instance, **kwargs):
    blog_page_changed(instance)
