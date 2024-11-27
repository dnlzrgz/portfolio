from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class NoteBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a note-like widget.
    """

    title = CharBlock(required=True)
    content = RichTextBlock(features=["h1", "h2", "h3", "link"])

    class Meta:
        icon = "bold"
        template = "blocks/note_block.html"


class StackListBlock(StructBlock):
    """
    Custom `StructBlock` fir displaying a list of items in
    a fun form factor.
    """

    stack_items = ListBlock(
        StructBlock(
            [
                ("Item", CharBlock(required=True)),
            ],
        ),
        label="Stack items",
    )

    class Meta:
        icon = "cog"
        template = "blocks/stack_list_block.html"


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for displaying an image with an associated caption
    in the form of a "widget".
    """

    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=True)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class ContactEmailBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a link with a contact email.
    """

    class Meta:
        icon = "mail"
        template = "blocks/contact_email_block.html"


class CalendarBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a calendar widget.
    """

    class Meta:
        icon = "calendar-alt"
        template = "blocks/calendar_block.html"


class TodoListBlock(StructBlock):
    default_tasks = ListBlock(
        StructBlock(
            [
                ("done", BooleanBlock(required=False)),
                ("label", CharBlock(required=True)),
            ],
        ),
        label="Defaul tasks",
    )

    class Meta:
        icon = "circle-check"
        template = "blocks/todo_list_block.html"


class AbstractBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a piece of generative art.
    """

    class Meta:
        icon = "view"
        template = "blocks/abstract_block.html"


class FeaturedProjectBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a featured project.
    """

    title = CharBlock()
    project = PageChooserBlock(
        page_type="projects.ProjectPage",
        required=True,
    )

    class Meta:
        icon = "doc-full"
        template = "blocks/featured_project_block.html"


class FeaturedBlogPostBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a featured blog post.
    """

    title = CharBlock()
    blog_post = PageChooserBlock(
        page_type="blog.BlogPostPage",
        required=True,
    )

    class Meta:
        icon = "doc-full"
        template = "blocks/featured_blog_post_block.html"


class SocialMediaLinksBlock(StructBlock):
    """
    Custom `StructBlock` for displaying a list of social media and other external links.
    """

    title = CharBlock(max_length=20)
    links = ListBlock(
        StructBlock(
            [
                ("title", CharBlock()),
                ("url", URLBlock()),
            ],
            label="links",
        )
    )

    class Meta:
        icon = "link-external"
        template = "blocks/social_media_links_block.html"
