from bakery.feeds import BuildableFeed
from blog.models import BlogPostPage


class RssFeed(BuildableFeed):
    title = "dnlzrgz - Blog"
    link = "/"
    description = "Lates posts from dnlzrgz's blog on software development with Python, Django, FastAPI and more."
    feed_url = "/rss.xml"
    build_path = "rss.xml"
    author_name = "dnlzrgz"
    categories = (
        "python",
        "django",
        "development",
        "web",
        "api",
        "microservices",
        "fast api",
    )
    feed_copyright = "Copyright ©2024, dnlzrgz"

    language = "en"

    def items(self):
        return BlogPostPage.objects.live().order_by("-first_published_at")[:20]

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
        return [tag.name for tag in item.tags.all()]
