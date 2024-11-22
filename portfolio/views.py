from bakery.views import BuildableTemplateView
from wagtail.contrib.sitemaps.views import sitemap


class Custom404View(BuildableTemplateView):
    build_path = "404.html"
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_code"] = "404"
        return context


class Custom500View(BuildableTemplateView):
    build_path = "500.html"
    template_name = "error.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_code"] = "500"
        return context


class RobotsView(BuildableTemplateView):
    build_path = "robots.txt"
    template_name = "robots.txt"


class SitemapView(BuildableTemplateView):
    build_path = "sitemap.xml"
    template_name = ""

    def get(self, request):
        return sitemap(request)
