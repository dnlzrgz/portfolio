from bakery.views import BuildableTemplateView
from wagtail.contrib.sitemaps.views import sitemap


class RobotsView(BuildableTemplateView):
    build_path = "robots.txt"
    template_name = "robots.txt"


class SitemapView(BuildableTemplateView):
    build_path = "sitemap.xml"
    template_name = ""

    def get(self, request):
        return sitemap(request)
