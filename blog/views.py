from django.contrib.syndication.views import Feed
from blog.models import BlogPostPage


class RssFeed(Feed):
    title = "Blog | dnlzrgz"
    link = "/blog/"
    description = ""
    author_name = "dnlzrgz"
    categories = ("django", "python", "go", "development", "backend")
    feed_copyright = "Copyright (c) 2024, dnlzrgz.com'"
    language = "en"

    def items(self):
        return BlogPostPage.objects.live().order_by("-first_published_at")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.tldr

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at

    def item_categories(self, item):
        return item.tags.all()
